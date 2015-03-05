# coding=utf-8
import json
import random
from django.http import HttpResponse

from ExpertSystem.models import *

__author__ = 'maxim'

parametr_values = []
attributes_values = []
relations= ['<', '<=', '>', '>=', '=', '!=']
logics = ['and', 'or']

def clear_db():
    Parameter.objects.all().delete()
    ParameterValue.objects.all().delete()
    Question.objects.all().delete()
    Rule.objects.all().delete()
    SysObject.objects.all().delete()
    Attribute.objects.all().delete()
    AttributeValue.objects.all().delete()
    System.objects.all().delete()
    Answer.objects.all().delete()


def insert_es():
    es = System(name="Экспертная система по выбору домашнего животного")
    es.save()


def insert_attr():
    es = System.objects.first()

    attr = Attribute(system=es, name="Размер")
    attr.save()

    attributeV = AttributeValue(system=es, attr=attr, value="Большой")
    attributeV.save()
    attributes_values.append(attributeV)

    attributeV = AttributeValue(system=es, attr=attr, value="Средний")
    attributeV.save()
    attributes_values.append(attributeV)

    attributeV = AttributeValue(system=es, attr=attr, value="Маленький")
    attributeV.save()
    attributes_values.append(attributeV)

    attr = Attribute(system=es, name="Цвет")
    attr.save()

    attributeV = AttributeValue(system=es, attr=attr, value="Синий")
    attributeV.save()
    attributes_values.append(attributeV)

    attributeV = AttributeValue(system=es, attr=attr, value="Белый")
    attributeV.save()
    attributes_values.append(attributeV)

    attributeV = AttributeValue(system=es, attr=attr, value="Черный")
    attributeV.save()
    attributes_values.append(attributeV)

    attr = Attribute(system=es, name="Шерсть")
    attr.save()

    attributeV = AttributeValue(system=es, attr=attr, value="Густая")
    attributeV.save()
    attributes_values.append(attributeV)

    attributeV = AttributeValue(system=es, attr=attr, value="Редкая")
    attributeV.save()
    attributes_values.append(attributeV)

    attributeV = AttributeValue(system=es, attr=attr, value="Прореженная лишаем")
    attributeV.save()
    attributes_values.append(attributeV)


def generate_literal():
    literal_param_v = random.choice(parametr_values)
    relation= random.choice(relations)

    return {
        'param': literal_param_v.param.id,
        'value': literal_param_v.id,
        'relation': relation
    }


def insert_rules():
    literals = []
    logic = []
    count = random.randint(1,5)
    for x in xrange(count):
        literals.append(generate_literal())
        if count - 1 > x:
            logic.append(random.choice(logics))

    conditions = {
        'literals': literals,
        'logic': logic,

    }

    results = []
    for x in xrange(1,3):
        results.append(get_attribute())
    type = Rule.ATTR_RULE
    rule = Rule(condition=json.dumps(conditions), result=json.dumps(results), type=type)
    rule.save()


def get_attribute():
    attribute_value = random.choice(attributes_values)
    attribute = attribute_value.attr # выбрали рандомный атрибут
    values = []
    #ждля него выбираем множество значений
    for attribute_value in attributes_values:
        if attribute_value.attr == attribute:
            values.append(attribute_value.id)
    return {
        'attribute': attribute.id,
        'values': values
    }


def insert_parameters():
    es = System.objects.first()

    p = Parameter(system=es, name="Нос")
    p.save()

    q = Question(system=es, body="Что вы любите есть?", type=Question.SELECT, parameter=p)
    q.save()
    pv = ParameterValue(system=es, param=p, value="В говне")
    pv.save()
    parametr_values.append(pv)

    pv = ParameterValue(system=es, param=p, value="Чистый")
    pv.save()
    parametr_values.append(pv)

    pv = ParameterValue(system=es, param=p, value="Отрезанный")
    pv.save()
    parametr_values.append(pv)

    p = Parameter(system=es, name="Усы")
    p.save()

    q = Question(system=es, body="Что вы любите пить?", type=Question.SELECT, parameter=p)
    q.save()
    pv = ParameterValue(system=es, param=p, value="Длинные")
    pv.save()
    parametr_values.append(pv)

    pv = ParameterValue(system=es, param=p, value="Обпаленные")
    pv.save()
    parametr_values.append(pv)

    pv = ParameterValue(system=es, param=p, value="Прореженные лишаем")
    pv.save()
    parametr_values.append(pv)

    p = Parameter(system=es, name="Хвост")
    p.save()

    q = Question(system=es, body="Что вы любите бить?", type=Question.SELECT, parameter=p)
    q.save()

    pv = ParameterValue(system=es, param=p, value="Длинные")
    pv.save()
    parametr_values.append(pv)

    pv = ParameterValue(system=es, param=p, value="Обрубили каблуком")
    pv.save()
    parametr_values.append(pv)


def run():
    clear_db()
    insert_es()
    insert_parameters()
    insert_attr()
    insert_rules()