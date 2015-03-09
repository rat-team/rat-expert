from django.shortcuts import render
from ExpertSystem.models import System, Question, Parameter
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_creation_session


@require_creation_session()
def add_answers(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])
    questions = Question.objects.filter(system=system)
    return render(request, "add_system/add_answers.html", {
        "questions": questions
    })


def insert_answers(request):
    pass