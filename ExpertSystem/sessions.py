SESSION_KEY = "ExpertSystem"


def init_session(request, system_id):
    SESSION = {
        "system_id": system_id,
        "selected_params": [],
        "asked_questions": [],
    }

    request.session.set(SESSION_KEY, SESSION)
