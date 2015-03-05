SESSION_KEY = "ExpertSystem"


def init_session(request, system_id):
    session = {
        "system_id": system_id,
        "selected_params": [],
        "asked_questions": [],
        "objects": []
    }

    request.session[SESSION_KEY] = session


def add_to_session(request, selected_params=None, asked_questions=None, objects=None):
    session = request.session.get(SESSION_KEY)
    if selected_params:
        session["selected_params"].extend(selected_params)
    if asked_questions:
        session["asked_questions"].extend(asked_questions)
    if objects:
        session["objects"].extend(objects)


def parse_session(session):
    return
