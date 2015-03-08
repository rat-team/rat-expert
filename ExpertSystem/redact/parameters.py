from django.shortcuts import render
from ExpertSystem.models import System, Parameter
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_creation_session


@require_creation_session()
def add_parameters(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])
    all_params = Parameter.objects.filter(system=system)

    params = []
    for param in all_params:
        params.append({
            "id": param.id,
            "name": param.name
        })

    return render(request, "add_system/add_parameters.html", {"params": params})