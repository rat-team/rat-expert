# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from ExpertSystem.models import System
from ExpertSystem.queries import add_weight_to_objects, update_session_attributes
from scripts.database import run
from ExpertSystem.models import Question
from ExpertSystem.models import Answer
from ExpertSystem.models import Parameter
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_session
from ExpertSystem.utils.parser import *
from ExpertSystem.utils.decorators import require_post_params


def index(request):
    if not request.GET.has_key("system_id") and not request.session.has_key(sessions.SESSION_KEY):
        systems = System.objects.all()
        return render(request, "systems.html", {"systems": systems})

    if not request.session.has_key(sessions.SESSION_KEY):
        system_id = request.GET.get("system_id")
        sessions.init_session(request, system_id)

    return next_question(request)


@require_session()
def next_question(request):
    session_dict = request.session.get(sessions.SESSION_KEY)
    system_id = session_dict["system_id"]
    selected_params = session_dict["selected_params"]
    asked_questions = session_dict["asked_questions"]

    system = System.objects.get(id=system_id)
    all_parameters = Parameter.objects.filter(system=system)

    # Берем все параметры
    for param in all_parameters:

        # Находим, какие еще не выясняли
        if param.id not in selected_params:

            questions = Question.objects.filter(parameter=param)

            #Проходим все вопросы у каждого параметра, смотрим какие еще не задавали и спрашиваем
            for question in questions:
                if question not in asked_questions:
                    answers = Answer.objects.filter(question=question)
                    ctx = {
                        "question": question,
                        "answers": answers,
                    }
                    return render(request, "question.html", ctx)

    return HttpResponse("THE END")

@require_session()
@require_post_params("answer", "question_id")
def answer(request):
    answer_id = request.POST.get("answer")
    question_id = request.POST.get("question_id")

    session = request.session.get(sessions.SESSION_KEY)
    if answer_id == "dont_know":
        sessions.add_to_session(request, asked_questions=[question_id])
        return next_question(request)

    answer = Answer.objects.get(id=answer_id)

    attrs = get_attributes(answer)
    update_session_attributes(session, attrs)
    #MAX(session, param_value)
    #ILUHA(session)

    sessions.add_to_session(request, asked_questions=question_id)

    return next_question(request)


def create_db(request):
    run()
    return HttpResponse(content="OK")


