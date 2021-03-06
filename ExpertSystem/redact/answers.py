# coding=utf-8
import json
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System, Question, Parameter, Answer
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_creation_session, require_post_params


@require_creation_session()
def add_answers(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])
    questions = Question.objects.filter(system=system, type=Question.SELECT)
    return render(request, "add_system/add_answers.html", {
        "questions": questions
    })


@require_http_methods(["POST"])
@require_post_params("form_data")
@require_creation_session()
@transaction.atomic
def insert_answers(request):
    """
    Добавление/редактирование ответов
    :param request:
    {
        "form_data": [
            {
                "id": id вопроса
                "answers": [
                    {
                        "id": id ответа, либо -1
                        "body": значение,
                        "parameter_value": значение параметра, устанавлимое этим ответом
                    }
                ]
            }
        ]
    }
    :return:
    """
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])

    form_data = json.loads(request.POST.get("form_data"))
    for question_element in form_data:
        question = Question.objects.get(id=question_element['id'], system=system)
        if len(question_element['answers']) > 0:
            for answer in question_element['answers']:
                a_id = answer['id']
                if a_id and int(a_id) != -1:
                    # Обновление вопроса
                    answer_element = Answer.objects.get(id=a_id)
                    answer_element.body = answer['body']
                    answer_element.parameter_value = answer['parameter_value']
                    answer_element.save()
                else:
                    # Создание вопроса
                    answer_element = Answer(question=question, body=answer['body'], parameter_value=answer['parameter_value'])
                    answer_element.save()
                pass
        else:
            # удалить все ответы для этого вопроса
            Answer.objects.filter(question=question).delete()
    response = {
        "code": 0,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

@require_http_methods(["POST"])
@require_post_params("id")
@require_creation_session()
@transaction.atomic
def delete_answer(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])

    id = request.POST.get("id")
    if id and int(id) > 0:
        Answer.objects.filter(id=id).delete()
        response = {
            "code": 0,
        }
    else:
        response = {
            "code": 1,
            "msg": "Неправильный запрос"
        }
    return HttpResponse(json.dumps(response), content_type="application/json")