# coding=utf-8
import json
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System, Parameter, Rule
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_creation_session, require_post_params


@require_creation_session()
def add_parameters(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])
    all_params = Parameter.objects.filter(system=system)

    params = []
    for param in all_params:
        print(str(param.id) + " " + param.name)
        params.append({
            "id": param.id,
            "name": param.name
        })

    return render(request, "add_system/add_parameters.html", {"params": params})


@require_http_methods(["POST"])
@require_post_params("form_data")
@require_creation_session()
@transaction.atomic
def insert_parameters(request):
    """
    Добавление/редактирование параметров
    :param request:
    {
        "form_data": [
            {
                "id": id параметра либо -1, если параметр новый и надо его создать
                "name": имя атрибута
            }
        ]
    }
    :return:
    """
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])

    form_data = json.loads(request.POST.get("form_data"))
    for param_json in form_data:
        if param_json["id"] and int(param_json["id"]) != -1:
            # Редактируем параметр
            try:
                parameter = Parameter.objects.get(id=param_json["id"])
            except Parameter.DoesNotExist:
                parameter = None

            if parameter:
                parameter.name = param_json["name"]
                parameter.save()
                continue

        # Создаем параметр
        Parameter.objects.create(name=param_json["name"], system=system)

    response = {
        "code": 0,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


@require_http_methods(["POST"])
@require_creation_session()
@require_post_params("id")
@transaction.atomic
def delete_parameter(request):
    """
    Удаление параметра
    :param request: id параметра
    :return:
    """
    param_id = request.POST.get("id")
    try:
        parameter = Parameter.objects.get(id=param_id)
        if not parameter:
            raise Parameter.DoesNotExist
    except Parameter.DoesNotExist:
        response = {
            "code": 0,
        }
        return HttpResponse(json.dumps(response), content_type="application/json")

    rules = Rule.objects.all()
    for rule in rules:
        results = json.loads(rule.result)
        condition = json.loads(rule.condition)

        param_in_condition = False
        for literal in condition['literals']:
            if literal['param'] == parameter.id:
                param_in_condition = True
                rule.delete()
                break

        if param_in_condition or rule.type != Rule.PARAM_RULE:
            continue
        else:
            for result in results:
                if result['parameter'] == parameter.id:
                    results.remove(result)

            if not results:
                rule.delete()
            else:
                rule.result = json.dumps(results)
                rule.save()

    parameter.delete()

    response = {
        "code": 0,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")