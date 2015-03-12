# coding=utf-8
import json
from ExpertSystem.models import Rule
from ExpertSystem.utils import sessions

RELATION_E = '='
RELATION_NE = '!='
RELATION_G = '>'
RELATION_L = '<'
RELATION_GE = '>='
RELATION_LE = '<='


def get_parameters(session_parameters):
    # добавляет в сессию параметры, пока находятся новые
    once_more = True
    while once_more:
        new_parameters = {}
        results = scan_rules(session_parameters, Rule.PARAM_RULE)

        if len(results) == 0:
            return

        for result in results:
            parameter = new_parameters.get(int(result['parameter']), [])
            parameter.append(result['values'])
            new_parameters[result['parameter']] = parameter
        once_more = add_params_to_session(session_parameters, new_parameters)


def get_attributes(session_parameters):
    # возвращает атрибуты
    attrs = {}
    results = scan_rules(session_parameters)
    for result in results:
        attrs[result['attribute']] = result['values']
    return attrs


def add_params_to_session(session_params, new_params):
    #  возвращает были ли добавлены новые параметры в сессию
    new = False
    for param, values in new_params.iteritems():
        session_param_values = session_params.get(param, [])
        for value in values:
            if value not in session_param_values:
                new = True
                session_param_values.append(value)
        session_params[param] = session_param_values
    return new


def scan_rules(param_dict, type=Rule.ATTR_RULE):
    # проверяет все правила и возвращает результат
    rules = Rule.objects.filter(type=type)
    results = []
    for rule in rules:
        condition = json.loads(rule.condition)
        literals = condition['literals']
        logic = condition['logic']
        results_list = []  # будет храниться результат выражений литералов
        for literal in literals:
            values_from_map = param_dict.get(literal['param'], [])
            result = False
            for value_from_map in values_from_map:
                if not result:
                    result = compare_param_values(literal['relation'], value_from_map, literal['value'])
                else:
                    break
            results_list.append(result)
        if process_logic_expression(logic, results_list):
            for rule_result in json.loads(rule.result):
                results.append(rule_result)
    return results


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

