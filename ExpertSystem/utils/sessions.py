# coding=utf-8
from ExpertSystem.models import System, SysObject

SESSION_KEY = "ExpertSystem"
SESSION_ES_CREATE_KEY = "ExpertSystem_create"


def init_session(request, system_id):
    system = System.objects.filter(id=system_id)
    sys_objects = SysObject.objects.filter(system=system)
    objects=[]
    for object in sys_objects:
        objects.append({
            "name": object.name,
            "weight": 0,
        })
    session = {
        "system_id": system_id,
        "selected_params": [],
        "asked_questions": [],
        "objects": objects
    }

    request.session[SESSION_KEY] = session


def add_to_session(request, asked_questions=None):
    session = request.session.get(SESSION_KEY)

    if asked_questions:
        session["asked_questions"] += asked_questions

    request.session[SESSION_KEY] = session


def clear_session(request):
    # if request.session.has_key(SESSION_KEY):
    #     del request.session[SESSION_KEY]
    request.session.clear()


def init_es_create_session(request, system_id):
    # Как только мы начали редактирование системы, или создали новую, мы записываем ее в сессию,
    # это значит, что мы в режиме редактирования и нужно не добавлять сущности, а изменять
    session = {
        "system_id": system_id,
    }

    request.session[SESSION_ES_CREATE_KEY] = session