from ExpertSystem.models import System, SysObject

SESSION_KEY = "ExpertSystem"


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


def add_to_session(request, selected_params=None, asked_questions=None, objects=None):
    session = request.session.get(SESSION_KEY)
    if selected_params:
        session["selected_params"] += selected_params
    if asked_questions:
        session["asked_questions"] += asked_questions
    if objects:
        session["objects"] += objects


def clear_session(request):
    request.session.clear()
