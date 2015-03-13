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
        cur.execute("DELETE FROM auth_user")
        cur.execute("DELETE FROM system")
        cur.execute("DELETE FROM attribute")
        cur.execute("DELETE FROM parameter")
        cur.execute("DELETE FROM question")
        cur.execute("DELETE FROM answer")
        cur.execute("DELETE FROM attribute_value")
        cur.execute("DELETE FROM sys_object")
        cur.execute("DELETE FROM rule")
        cur.execute("SET foreign_key_checks = 1")

    user = User.objects.create(username="admin", email="admin@admin.admin", is_superuser=True, is_staff=True)
    user.set_password("admin")
    user.save()
    user2 = User.objects.create(username="maxmyalkin", email="max@myalkin.black")
    user2.set_password("20")
    user2.save()
    system = System.objects.create(name="System 1", user=user)
    system2 = System.objects.create(name="System 2", user=user2)

    # Параметр шерсть
    fur_param = Parameter.objects.create(system=system, name="Предпочтение в типе шерсти")
    long_fur = "длинная"
    short_fur = "короткая"

    # Параметр цвет
    color_param = Parameter.objects.create(system=system, name="Предпочтения в цвете")
    warm_color = "теплые"
    cold_color = "холодные"

    # Параметр аллергия (!!!! для правила параметр-параметр !!!!)
    allerg_param = Parameter.objects.create(system=system, name="Склонность к аллергии")
    not_prone = "не склонен"
    prone = "склонен"

    # Атрибуты шерсти
    fur_length_attr = Attribute.objects.create(system=system, name="Длина шерсти")
    long_fur_attr = AttributeValue.objects.create(system=system, attr=fur_length_attr, value="Длинная")
    short_fur_attr = AttributeValue.objects.create(system=system, attr=fur_length_attr, value="Короткая")

     # Атрибуты цвета
    color_attr = Attribute.objects.create(system=system, name="Цвет")
    color_white_attr = AttributeValue.objects.create(system=system, attr=color_attr, value="Белый")
    color_black_attr = AttributeValue.objects.create(system=system, attr=color_attr, value="Черный")



    # объекты

    # черная и белая кошка с короткой шерстью
    cat = SysObject.objects.create(system=system, name="Кошка")
    cat.attributes.add(short_fur_attr)
    cat.attributes.add(color_black_attr)
    cat.attributes.add(color_white_attr)

    # белая собака с длинной шерстью
    dog = SysObject.objects.create(system=system, name="Собака")
    dog.attributes.add(long_fur_attr)
    dog.attributes.add(color_white_attr)


    question_1_parameter_1 = Question.objects.create(
        parameter=fur_param, body="Какие типы шерсти вам нравятся больше?",
        system=system, type=0
    )

    answer_1_question_1 = Answer.objects.create(body="Больше нравится длинная шерсть",
                                                question=question_1_parameter_1,
                                                parameter_value=long_fur)
    answer_2_question_1 = Answer.objects.create(body="Больше нравится короткая шерсть",
                                                question=question_1_parameter_1,
                                                parameter_value=short_fur)

    question_2 = Question.objects.create(
        parameter=color_param, body="Какие цвета вы предпочитаете?",
        system=system, type=0
    )

    answer_1_question_2 = Answer.objects.create(body="Теплые",
                                                question=question_2,
                                                parameter_value=warm_color)
    answer_2_question_2 = Answer.objects.create(body="Холодные",
                                                question=question_2,
                                                parameter_value=cold_color)

    type = Rule.ATTR_RULE

    # правило - короткая шерсть
    condition = {
        "literals": [
            {"param": fur_param.id, "relation": "=", 'value': short_fur}
        ],
        'logic': []
    }

    condition = json.dumps(condition)

    result = [{
        'attribute': fur_length_attr.id,
        'values': [short_fur_attr.id]
    }]

    result = json.dumps(result)

    rule_1 = Rule.objects.create(condition=condition, result=result, type=type, system=system)



    # правило - длинная шерсть
    condition = {
        "literals": [
            {"param": fur_param.id, "relation": "=", 'value': long_fur}
        ],
        'logic': []
    }
    condition = json.dumps(condition)

    result = [{
        'attribute': fur_length_attr.id,
        'values': [long_fur_attr.id]
    }]
    result = json.dumps(result)

    rule_2 = Rule.objects.create(condition=condition, result=result, type=type, system=system)

    # правило - черный цвет - холодный
    condition = {
        "literals": [
            {"param": color_param.id, "relation": "=", 'value': cold_color}
        ],
        'logic': []
    }

    condition = json.dumps(condition)

    result = [{
        'attribute': color_attr.id,
        'values': [color_black_attr.id, color_white_attr.id]
    }]

    result = json.dumps(result)

    rule_3 = Rule.objects.create(condition=condition, result=result, type=type, system=system)

    # правило - белый цвет - теплый
    condition = {
        "literals": [
            {"param": color_param.id, "relation": "=", 'value': warm_color}
        ],
        'logic': []
    }
    condition = json.dumps(condition)

    result = [{
        'attribute': color_attr.id,
        'values': [color_white_attr.id]
    }]
    result = json.dumps(result)

    rule_4 = Rule.objects.create(condition=condition, result=result, type=type, system=system)

    # правило - длинная шерсть - не склонен к аллергии
    param_type = Rule.PARAM_RULE

    condition = {
        "literals": [
            {"param": fur_param.id, "relation": "=", 'value': long_fur},
            {"param": fur_param.id, "relation": "<=", 'value': short_fur},
        ],
        'logic': ["or"]
    }
    condition = json.dumps(condition)

    result = [{
        'parameter': allerg_param.id,
        'values': not_prone
    }]
    result = json.dumps(result)

    rule_5 = Rule.objects.create(condition=condition, result=result, type=param_type, system=system)