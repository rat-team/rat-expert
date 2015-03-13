# coding=utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ExpertSystem.models import System
from ExpertSystem.utils.sessions import clear_session
from ExpertSystem.queries import update_session_attributes
from ExpertSystem.models import Question
from ExpertSystem.models import Answer
from ExpertSystem.models import Parameter
from ExpertSystem.utils.decorators import require_session
from ExpertSystem.utils.parser import *
from ExpertSystem.utils.decorators import require_post_params


@login_required(login_url="/login/")
def index(request):
    sessions.clear_es_create_session(request)
    if sessions.SESSION_KEY not in request.session:
        system_id = request.GET.get("system_id", None)
        if not system_id:
            systems = System.objects.all()
            return render(request, "systems.html", {"systems": systems, "user_id": request.user.id})
        else:
            sessions.init_session(request, system_id)

    return next_question(request)


def reset(request):
    """
    Очищает сессию, стартует тестирование заново
    """
    system_id = request.GET.get('system_id')
    clear_session(request)
    return HttpResponseRedirect("/index/?system_id=" + system_id)

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

        param_values = selected_params.get(str(param.id), None)

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

    return render(request, "final.html", {"system_id": system.id, "table": session_dict["objects"]})

@require_session()
@require_post_params("answer", "question_id")
def answer(request):
    answer_id = request.POST.get("answer")
    question_id = request.POST.get("question_id")

    session_dict = request.session.get(sessions.SESSION_KEY, None)
    selected_params = session_dict['selected_params']

    question = Question.objects.get(id=question_id)
    param_id = question.parameter.id
    param_values = selected_params.get(param_id, [])

    if question.type == 0:
        answer = Answer.objects.get(id=answer_id)
        if not answer.parameter_value or answer.parameter_value == "":
            return skip_question(request, question_id)
        param_values.append(answer.parameter_value)
    else:
        # Здесь answer_id - текст ответа
        param_values.append(answer_id)

    selected_params[param_id] = param_values

    get_parameters(selected_params)

    attrs = get_attributes(selected_params)

    sessions.add_to_session(request, asked_questions=[int(question_id), ], selected_params=selected_params)

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


@login_required(login_url="/login/")
def main_menu(request):
    sessions.clear_session(request)
    return redirect('ExpertSystem.views.index')


@login_required(login_url="/login/")
@require_session()
def skip_question(request, question_id):
    try:
        sessions.add_to_session(request, asked_questions=[int(question_id)])
    except ValueError:
        pass
    return HttpResponseRedirect("/index")

@login_required(login_url="/login/")
def presentation(request):
    return render(request, "presentation.html")

def faq(request):
    return render(request, "FAQ.html")

@require_http_methods(["GET"])
@login_required(login_url="/login/")
def delete_system(request, system_id=None):
    if system_id:
        try:
            system = System.objects.get(id=system_id)
            user_id = User.objects.get(id=system.user_id).id
        except System.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'System doesn\'t exist'}), content_type='application/json')
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'error': 'User doesn\'t exist'}), content_type='application/json')

        if request.user.id == user_id:
            system.delete()
            return HttpResponse(json.dumps({'OK': 'Deleted'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'error': 'You can\'t delete this system'}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'error': 'No system id'}), content_type='application/json')
