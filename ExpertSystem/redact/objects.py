# coding=utf-8
import json
from django import forms
from django.db import transaction
from django.forms import Select
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System
from ExpertSystem.models import SysObject
from ExpertSystem.models import AttributeValue
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_creation_session
from ExpertSystem.utils.decorators import require_post_params


@require_creation_session()
def add_objects(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])
    all_objects = SysObject.objects.filter(system=system)

    attribute_values = AttributeValue.objects.filter(system=system)

    # attribute_values = forms.ModelChoiceField(widget=Select(attrs={'class': "form-control"}),
    #                                        queryset=AttributeValue.objects.filter(system=system),
    #                                        label="Атрибут-значение")
    #
    return render(request, "add_system/objects_page/add_objects.html", {
        "objects": all_objects,
        "attribute_values": attribute_values,
    })


@require_http_methods(["POST"])
@require_post_params("form_data")
@require_creation_session()
@transaction.atomic
def insert_objects(request):
    """
    Добавляет объекты
    :param request: {
        "form_data": [
            {
                "id": id объекта либо -1, если объект новый и надо его создать
                "name": имя объекта
                "attribute_values": [
                    id AttributeValue, id, id, ...
                ]
            }, ...
        ]
    }
    :return:
    """
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])
    formdata = json.loads(request.POST.get('form_data'))

    SysObject.objects.filter(system=system).delete()

    for objectJSON in formdata:
        object = SysObject.objects.create(name=objectJSON["name"], system=system)
        for attribute_value_id in objectJSON["attribute_values"]:
            attribute_value = AttributeValue.objects.get(id=attribute_value_id)
            object.attributes.add(attribute_value)
        object.save()

    response = {
        "code": 0,
    }

    return HttpResponse(json.dumps(response), content_type="application/json")