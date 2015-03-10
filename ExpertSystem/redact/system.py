# coding=utf-8
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_post_params
from scripts.recreate import recreate


def create_db(request):
    recreate()
    return HttpResponse(content="OK")


def add_system(request, **kwargs):

    if "system_id" in kwargs:
        # Если выбрали редактирование конкретной системы
        #TODO если редактируем, проверить, что это мы ее создавали
        system_id = kwargs["system_id"]
        sessions.init_es_create_session(request, system_id)
        system = System.objects.get(id=system_id)
        return render(request, "add_system/add_system.html", {"system": system})

    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    if session:
        # Если внутри редактирования вернулись на страницу создания системы
        system = System.objects.get(id=session["system_id"])
        return render(request, "add_system/add_system.html", {"system": system})

    # Иначе все по нулям
    return render(request, "add_system/add_system.html")


@login_required(login_url="/login/")
@require_http_methods(["POST"])
@require_post_params("system_name")
def insert_system(request):

    response = {
        "code": 0,
    }

    system_name = request.POST.get("system_name")
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    if session:
        system = System.objects.get(id=session["system_id"])
        system.name = system_name
        system.save()
        return HttpResponse(json.dumps(response), content_type="application/json")

    system = System.objects.create(name=system_name, user=request.user)
    sessions.init_es_create_session(request, system.id)
    return HttpResponse(json.dumps(response), content_type="application/json")