from django.shortcuts import render
from ExpertSystem import sessions
from ExpertSystem.models import System
from decorators import require_session


def index(request):

    if not request.GET.has_key("system") and not request.session.has_key(sessions.SESSION_KEY):
        systems = System.objects.all()
        return render(request, "index.html", {"systems": systems})

    if not request.session.has_key(sessions.SESSION_KEY):
        system_id = request.session.get("system")
        sessions.init_session(request, system_id)

    return next_question(request)


@require_session()
def next_question(request):
    system = request.session.get(sessions.SESSION_KEY)

    pass


def answer(request):

    #session.set

    return next_question(request)