# coding=utf-8
import json
from ExpertSystem.models import Rule

RELATION_E = '='
RELATION_NE = '!='
RELATION_G = '>'
RELATION_L = '<'
RELATION_GE = '>='
RELATION_LE = '<='


def get_attributes(answer):
    # возвращает тьюпл из параметров и атрибутов - пока что только атрибуты
    if answer == "dont_know":
        return {}
    parameter_value = answer.parameter_value
    param_dict = make_param_dict([parameter_value])
    return scan_rules(param_dict)

def make_param_dict(params_values):
    # создание карты которая ид параметра соотносит список его значений
    param_to_values = {}
    for param_value in params_values:
        param_id = param_value.param.id  # id параметра
        param_to_values[param_id]= param_value.value
    return param_to_values


def scan_rules(param_dict):
    # проверяет все правила и возвращает атрибуты, которые надо применить
    rules = Rule.objects.all()
    attrs = {}
    for rule in rules:
        condition = json.loads(rule.condition)
        literals = condition['literals']
        logic = condition['logic']
        results_list = []  # будет храниться результат выражений литералов
        for literal in literals:
            value_from_map = param_dict.get(literal['param'], None)
            if value_from_map:
                results_list.append(compare_param_values(literal['relation'], value_from_map, literal['value']))
            else:
                results_list.append(False)
        if process_logic_expression(logic, results_list):
            results = json.loads(rule.result)
            for result in results:
                attrs[result['attribute']] = result['values']
    return attrs


def compare_param_values(relation, v1, v2):
    if relation == RELATION_E:
        return v1 == v2
    if relation == RELATION_G:
        return v1 > v2
    if relation == RELATION_L:
        return v1 < v2
    if relation == RELATION_GE:
        return v1 >= v2
    if relation == RELATION_LE:
        return v1 <= v2
    if relation == RELATION_NE:
        return v1 != v2


def process_logic_expression(logic_ops, boolean_list):
    # возвращает результат логического выражения литералов
    if len(logic_ops) == 0:
        return boolean_list[0]
    if len(logic_ops) > 0 and len(logic_ops) == len(boolean_list) - 1:
        expression_str = ''
        for x in xrange(len(boolean_list)):
            expression_str += str(boolean_list[x])
            if x < len(boolean_list) - 1:
                expression_str += " " + logic_ops[x] + " "
        return eval(expression_str)

