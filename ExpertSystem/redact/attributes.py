# coding=utf-8
import json
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System, Attribute, AttributeValue, SysObject, Rule
from ExpertSystem.redact.utils import get_system
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_creation_session, require_post_params
from ExpertSystem.utils.log_manager import log


@require_creation_session()
def add_attributes(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)

    system = get_system(session, request.user.id)
    if not system:
        return redirect("/reset/")

    all_attributes = Attribute.objects.filter(system=system)
    attributes = []
    for attribute in all_attributes:
        attr_values = AttributeValue.objects.filter(attr=attribute)
        values = []
        for value in attr_values:
            values.append({"id": value.id, "value": value.value})
        attributes.append({
            "id": attribute.id,
            "name": attribute.name,
            "values": values,
        })

    return render(request, "add_system/add_attributes.html", {"attributes": attributes})


@require_http_methods(["POST"])
@require_post_params("form_data")
@require_creation_session()
@transaction.atomic
def insert_attributes(request):
    """
    Добавление/редактирование атрибутов
    :param request:
    {
        "form_data": [
            {
                "id": id атрибута либо -1, если атрибут новый и надо его создать
                "name": имя атрибута
                "values": [
                    {
                        "id": id AttributeValue, либо -1
                        "value": значение
                    }
                ]
            }
        ]
    }
    :return:
    """
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = get_system(session, request.user.id)
    if not system:
        response = {
            "code": 1,
            "msg": u"Что-то пошло не так. Попробуйте обновить страницу."
        }

        return HttpResponse(json.dumps(response), content_type="application/json")

    form_data = json.loads(request.POST.get("form_data"))
    for attr_json in form_data:
        try:
            attr_id = int(attr_json.get("id"))
        except ValueError as e:
            log.exception(e)
            continue

        if not attr_json["name"]:
            response = {
                "code": 1,
                "msg": u"Заполните названия всех атрибутов, пожалуйста"
            }

            return HttpResponse(json.dumps(response), content_type="application/json")

        elif attr_id != -1:
            # Редактируем атрибут
            attribute = Attribute.objects.get(id=attr_id)
            attribute.name = attr_json["name"]
            attribute.save()
            # Обновляем значения:
            # TODO: добавить проверку values
            added_values = []
            for val in attr_json["values"]:
                if val["id"] and int(val["id"]) != -1:
                    attribute_value = AttributeValue.objects.get(id=val["id"])
                    if not val["value"]:
                        attribute_value.delete()
                        continue
                else:
                    attribute_value = AttributeValue(system=system, attr=attribute)
                    if not val["value"]:
                        continue

                if val["value"] in added_values:
                    continue

                added_values.append(val["value"])
                attribute_value.value = val["value"]
                attribute_value.save()

        else:
            # Создаем атрибут
            attribute = Attribute.objects.create(name=attr_json["name"], system=system)
            for val in attr_json["values"]:
                AttributeValue.objects.create(system=system, attr=attribute, value=val["value"])

    response = {
        "code": 0,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


@require_http_methods(["POST"])
@require_creation_session()
@require_post_params("id")
@transaction.atomic
def delete_attribute_value(request):
    """
    Удаляет значение атрибута
    :param request: "id" в запросе
    :return:
    """
    attribute_value_id = request.POST.get("id")

    if attribute_value_id:
        _delete_attribute_value(attribute_value_id)

    response = {
        "code": 0,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


def _delete_attribute_value(attribute_value_id):
    try:
        attribute_value_id = int(attribute_value_id)
        attribute_value = AttributeValue.objects.get(id=attribute_value_id)
    except ValueError as e:
        log.exception(e)
        return
    except AttributeValue.DoesNotExist:
        return

    rules = Rule.objects.filter(type=Rule.ATTR_RULE)
    for rule in rules:
        results = json.loads(rule.result)
        for result in results:

            updated_values = []

            for value in result["values"]:
                if value != attribute_value_id:
                    updated_values.append(value)

            if not updated_values:
                results[:] = [d for d in results if d != result]
            else:
                result["values"] = updated_values

        if not results:
            rule.delete()
        else:
            rule.result = json.dumps(results)
            rule.save()

    attribute_value.delete()


@require_http_methods(["POST"])
@require_creation_session()
@require_post_params("id")
@transaction.atomic
def delete_attribute(request):
    """
    Удаление атрибута
    :param request: id атрибута
    :return:
    """
    try:
        attribute_id = int(request.POST.get("id"))
        attribute = Attribute.objects.get(id=attribute_id)
        attribute_values = attribute.attributevalue_set.all()
    except (ValueError, Attribute.DoesNotExist) as e:
        log.exception(e)
        response = {
            "code": 1,
            "msg": u"Что-то пошло не так. Попробуйте обновить страницу."
        }

        return HttpResponse(json.dumps(response), content_type="application/json")

    for attr_val in attribute_values:
        _delete_attribute_value(attr_val.id)

    attribute.delete()

    response = {
        "code": 0,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")