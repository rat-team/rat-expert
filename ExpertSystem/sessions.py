SESSION_KEY = "ExpertSystem"


def init_session(request):
    SESSION = {
        "system_id": -1,
        "selected_params": [],
        "asked_questions": [],
    }

    request.session.set(SESSION_KEY, SESSION)
