# coding=utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System, SysObject
from ExpertSystem.utils.sessions import clear_session
from ExpertSystem.queries import update_session_attributes
from scripts.database import run
from ExpertSystem.models import Question
from ExpertSystem.models import Answer
from ExpertSystem.models import Parameter
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_session
from ExpertSystem.utils.parser import *
from ExpertSystem.utils.decorators import require_post_params
from scripts.recreate import recreate


@login_required(login_url="/login/")
def index(request):
    if sessions.SESSION_KEY not in request.session:
        if "system_id" not in request.GET:
            systems = System.objects.all()
            return render(request, "systems.html", {"systems": systems, "user_id": request.user.id})
        else:
            system_id = request.GET.get("system_id")
            sessions.init_session(request, system_id)

    return next_question(request)


def reset(request):
    """
    Очищает сессию, стартует тестирование заново
    """
    clear_session(request)
    return HttpResponseRedirect("/index")

@csrf_exempt
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                return HttpResponse(json.dumps({"status": "ERROR", "error": u"Неправильные данные"}), content_type="application/json")
            else:
                login(request, user)
                return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "ERROR", "error": u"Мало данных"}), content_type="application/json")
    else:
        return render(request, "auth/login.html")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and email and password:
            try:
                user = User.objects.get(username=username)
                if user:
                    return HttpResponse(json.dumps({"status": "ERROR", "error": u"Никнейм занят"}), content_type="application/json")
            except User.DoesNotExist:
                user = User.objects.create(email=email, username=username)
                user.set_password(request.POST["password"])
                user.save()

                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return HttpResponse(json.dumps({"status": "OK"}), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"status": "ERROR", "error": u"Ошибочка вышла"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "ERROR", "error": u"Мало данных"}, content_type="application/json"))
    else:
        return render(request, "auth/registration.html")


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

        param_values = selected_params.get(param.id, None)

        # Находим, какие еще не выясняли
        if not param_values:

            questions = Question.objects.filter(parameter=param)

            #Проходим все вопросы у каждого параметра, смотрим какие еще не задавали и спрашиваем
            for question in questions:
                if question.id not in asked_questions:
                    answers = Answer.objects.filter(question=question)
                    ctx = {
                        "question": question,
                        "answers": answers,
                        "table": session_dict["objects"]
                    }
                    return render(request, "question.html", ctx)

    return render(request, "final.html", {"table": session_dict["objects"]})

@require_session()
@require_post_params("answer", "question_id")
def answer(request):
    answer_id = request.POST.get("answer")
    question_id = request.POST.get("question_id")

    if answer_id == "dont_know":
        sessions.add_to_session(request,
                                asked_questions=[int(question_id), ])
        return HttpResponseRedirect("/index")

    answer = Answer.objects.get(id=answer_id)

    session_dict = request.session.get(sessions.SESSION_KEY, None)
    selected_params = session_dict['selected_params']
    param_id = answer.question.parameter.id
    param_values = selected_params.get(param_id, None)
    if not param_values:
        param_values = []
    param_values.append(answer.parameter_value)
    selected_params[param_id] = param_values

    get_parameters(request)

    attrs = get_attributes(request)

    sessions.add_to_session(request, asked_questions=[int(question_id), ])

    request.session[sessions.SESSION_KEY] = update_session_attributes(
        request.session.get(sessions.SESSION_KEY), attrs
    )

    return HttpResponseRedirect("/index")


@login_required(login_url="/login/")
def creators(request):
    return render(request, "creators.html")


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("/login/")