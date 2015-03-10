# coding=utf-8
import json
from django import forms
from django.db import transaction
from django.forms import Select
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System
from ExpertSystem.models import Parameter
from ExpertSystem.models import Question
from ExpertSystem.models import SysObject
from ExpertSystem.models import AttributeValue
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_creation_session
from ExpertSystem.utils.decorators import require_post_params


@require_creation_session()
def add_questions(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])
    all_parameters = Parameter.objects.filter(system=system)

    parameters = []

    for param in all_parameters:
        param_dict = {
            "id": param.id,
            "name": param.name,
            "questions": [],
        }
        param_questions = Question.objects.filter(parameter=param)
        for question in param_questions:
            param_dict["questions"].append(question)

        parameters.append(param_dict)

    return render(request, "add_system/questions_page/add_questions.html", {
        "parameters": parameters,
    })


@require_http_methods(["POST"])
@require_post_params("id")
@require_creation_session()
@transaction.atomic
def delete_question(request):
    id = request.POST.get("id")
    Question.objects.get(id=id).delete()
    response = {
        "code": 0,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


@require_http_methods(["POST"])
@require_post_params("form_data")
@require_creation_session()
@transaction.atomic
def insert_questions(request):
    """
    Добавляет объекты
    :param request: {
        "form_data": [
            {
                "id": id параметра,
                "questions": [
                    {
                        "id": id вопроса, либо -1, если вопрос новый
                        "type": тип вопроса (0 или 1),
                        "body": текст вопроса
                    }, ...
                ]
            }, ...
        ]
    }
    :return:
    """
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])
    formdata = json.loads(request.POST.get('form_data'))

    for parameterJSON in formdata:
        parameter = Parameter.objects.get(id=parameterJSON["id"])
        for questionJSON in parameterJSON["questions"]:
            question_id = questionJSON["id"]
            if question_id and question_id != "-1":
                question = Question.objects.get(id=question_id)
            else:
                question = Question(system=system, parameter=parameter)
            question.type = questionJSON["type"]
            question.body = questionJSON["body"]
            question.save()

    response = {
        "code": 0,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")