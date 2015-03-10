# coding=utf-8
import json
from django import forms
from django.db import transaction
from django.forms import Select
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from ExpertSystem.models import System, Rule, Parameter, Attribute
from ExpertSystem.models import SysObject
from ExpertSystem.models import AttributeValue
from ExpertSystem.utils import sessions
from ExpertSystem.utils.decorators import require_creation_session
from ExpertSystem.utils.decorators import require_post_params


@require_creation_session()
def add_rules(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])
    all_rules = Rule.objects.filter(system=system)
    all_parameters = Parameter.objects.filter(system=system)
    all_attribute_values = AttributeValue.objects.filter(system=system)

    rules = []
    for rule in all_rules:
        condition = json.loads(rule.condition)
        condition["logic"] = [None, ] + condition["logic"]
        zipped_logic = zip(condition["literals"], condition["logic"])
        condition["zipped_literal_logic"] = zipped_logic

        result = json.loads(rule.result)

        results = []
        if rule.type == 1:
            for res in result:
                for value in res["values"]:
                    attribute_value = AttributeValue.objects.get(id=value)
                    results.append(attribute_value)
        else:
            results = result

        ruleJSON = {
            "type": rule.type,
            "result": results,
            "condition": condition
        }

        rules.append(ruleJSON)

    return render(request, "add_system/rules_page/add_rules.html", {
        "rules": rules,
        "parameters": all_parameters,
        "attribute_values": all_attribute_values
    })


def insert_rules(request):
    pass