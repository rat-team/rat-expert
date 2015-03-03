from django.shortcuts import render
from ExpertSystem import sessions
from decorators import require_session


def index(request):
    if request.session.has_key(sessions.SESSION_KEY):
        return next_question(request)
    return render()


@require_session()
def next_question(request):
    pass


def answer(request):

    #session.set

    return next_question(request)