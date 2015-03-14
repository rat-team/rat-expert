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


@require_creation_session()
@require_http_methods(["POST"])
@require_post_params("form_data")
@transaction.atomic
def insert_rules(request):
    session = request.session.get(sessions.SESSION_ES_CREATE_KEY)
    system = System.objects.get(id=session["system_id"])

    Rule.objects.filter(system=system).delete()

    form_data = request.POST.get("form_data")
    for rule_data in json.loads(form_data):
        condition  = rule_data["condition"]
        literals = []
        for literal in condition["literals"]:
            literals.append({
                "relation": literal["relation"],
                "value": literal["value"],
                "param": int(literal["param"])
            })
        condition["literals"] = literals
        if len(condition["logic"]) == len(condition["literals"]):
            del(condition["logic"])
        type = rule_data["type"]
        result_data = rule_data["result"]
        if int(type) == 1:
            result_map = {}
            # Нужно найти AttributeValue
            for attr_value_id in result_data:
                attribute_value = AttributeValue.objects.get(id=attr_value_id)
                attr_id = attribute_value.attr.id
                if not result_map.has_key(attr_id):
                    result_map[attr_id] = []
                result_map[attr_id].extend([attribute_value.id])

            result = []
            for key in result_map.iterkeys():
                result_elem = {
                    "attribute": key,
                    "values": result_map[key],
                }
                result.append(result_elem)

        else:
            result = []
            for res in result_data:
                resJSON = {
                    "parameter": int(res["parameter"]),
                    "values": res["values"]
                }
                result.append(resJSON)

        Rule.objects.create(
            condition=json.dumps(condition),
            result=json.dumps(result),
            type=int(type),
            system=system
        )

    response = {
        "code": 0,
    }
    return HttpResponse(json.dumps(response), content_type="application/json")