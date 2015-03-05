SESSION_KEY = "ExpertSystem"


def init_session(request, system_id):
    session = {
        "system_id": system_id,
        "selected_params": [],
        "asked_questions": []
    }

    request.session.set(SESSION_KEY, session)


def parse_session(session):
    return
