# coding=utf-8
import MySQLdb as mdb
import json
from ExpertSystem.models import *


def recreate():

    con = mdb.connect('localhost', 'es', 'es', 'es', init_command='set names UTF8')

    with con:
        #Очистка
        cur = con.cursor()
        cur.execute("SET foreign_key_checks = 0")
        cur.execute("DELETE FROM system")
        cur.execute("DELETE FROM attribute")
        cur.execute("DELETE FROM parameter")
        cur.execute("DELETE FROM question")
        cur.execute("DELETE FROM parameter_value")
        cur.execute("DELETE FROM answer")
        cur.execute("DELETE FROM attribute_value")
        cur.execute("DELETE FROM sys_object")
        cur.execute("DELETE FROM rule")
        cur.execute("SET foreign_key_checks = 1")

    system = System.objects.create(name="System 1")

    # Параметр шерсть
    parameter_1 = Parameter.objects.create(system=system, name="Предпочтение в типе шерсти")
    parameter_1_value_1 = ParameterValue.objects.create(system=system, param=parameter_1, value="Длинношерстный")
    parameter_1_value_2 = ParameterValue.objects.create(system=system, param=parameter_1, value="Короткошерстный")

    # Параметр цвет
    parameter_2 = Parameter.objects.create(system=system, name="Предпочтения в цвете")
    parameter_2_value_1 = ParameterValue.objects.create(system=system, param=parameter_2, value="Теплые цвета")
    parameter_2_value_2 = ParameterValue.objects.create(system=system, param=parameter_2, value="Холодные цвета")


    # Атрибуты шерсти
    attribute_1 = Attribute.objects.create(system=system, name="Длина шерсти")
    attribute_1_value_1 = AttributeValue.objects.create(system=system, attr=attribute_1, value="Длинная")
    attribute_1_value_2 = AttributeValue.objects.create(system=system, attr=attribute_1, value="Короткая")

     # Атрибуты цвета
    attribute_2 = Attribute.objects.create(system=system, name="Цвет")
    attribute_2_value_1 = AttributeValue.objects.create(system=system, attr=attribute_2, value="Белый")
    attribute_2_value_2 = AttributeValue.objects.create(system=system, attr=attribute_2, value="Черный")



    # объекты

    # черная и белая кошка с короткой шерстью
    cat = SysObject.objects.create(system=system, name="Кошка")
    cat.attributes.add(attribute_1_value_2)
    cat.attributes.add(attribute_2_value_2)
    cat.attributes.add(attribute_1_value_1)

    # белая собака с длинной шерстью
    dog = SysObject.objects.create(system=system, name="Собака")
    dog.attributes.add(attribute_1_value_1)
    dog.attributes.add(attribute_2_value_1)


    question_1_parameter_1 = Question.objects.create(
        parameter=parameter_1, body="Какие типы шерсти вам нравятся больше?",
        system=system, type=0
    )

    answer_1_question_1 = Answer.objects.create(body="Больше нравится длинная шерсть",
                                                question=question_1_parameter_1,
                                                parameter_value=parameter_1_value_1)
    answer_2_question_1 = Answer.objects.create(body="Больше нравится короткая шерсть",
                                                question=question_1_parameter_1,
                                                parameter_value=parameter_1_value_2)

    question_2 = Question.objects.create(
        parameter=parameter_2, body="Какие цвета вы предпочитаете?",
        system=system, type=0
    )

    answer_1_question_2 = Answer.objects.create(body="Теплые",
                                                question=question_2,
                                                parameter_value=parameter_2_value_1)
    answer_2_question_2 = Answer.objects.create(body="Холодные",
                                                question=question_2,
                                                parameter_value=parameter_2_value_2)

    type = Rule.ATTR_RULE

    # правило - короткая шерсть
    condition = {
        "literals": [
            {"param": parameter_1.id, "relation": "=", 'value': parameter_1_value_2.value}
        ],
        'logic': []
    }

    condition = json.dumps(condition)

    result = [{
        'attribute': attribute_1.id,
        'values': [attribute_1_value_2.id]
    }]

    result = json.dumps(result)

    rule_1 = Rule.objects.create(condition=condition, result=result, type=type)



    # правило - длинная шерсть
    condition = {
        "literals": [
            {"param": parameter_1.id, "relation": "=", 'value': parameter_1_value_1.value}
        ],
        'logic': []
    }
    condition = json.dumps(condition)

    result = [{
        'attribute': attribute_1.id,
        'values': [attribute_1_value_1.id]
    }]
    result = json.dumps(result)

    rule_2 = Rule.objects.create(condition=condition, result=result, type=type)



    # правило - черный цвет - холодный
    condition = {
        "literals": [
            {"param": parameter_2.id, "relation": "=", 'value': parameter_2_value_2.value}
        ],
        'logic': []
    }

    condition = json.dumps(condition)

    result = [{
        'attribute': attribute_2.id,
        'values': [attribute_2_value_2.id]
    }]

    result = json.dumps(result)

    rule_3 = Rule.objects.create(condition=condition, result=result, type=type)



    # правило - белый цвет - теплый
    condition = {
        "literals": [
            {"param": parameter_2.id, "relation": "=", 'value': parameter_2_value_1.value}
        ],
        'logic': []
    }
    condition = json.dumps(condition)

    result = [{
        'attribute': attribute_2.id,
        'values': [attribute_2_value_1.id]
    }]
    result = json.dumps(result)

    rule_4 = Rule.objects.create(condition=condition, result=result, type=type)


