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

    attributeV = AttributeValue(system=es, attr=attr, value="Коричневый")
    attributeV.save()
    attributes_values.append(attributeV)

    attributeV = AttributeValue(system=es, attr=attr, value="Белый")
    attributeV.save()
    attributes_values.append(attributeV)

    attributeV = AttributeValue(system=es, attr=attr, value="Красный")
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


def generate_literal():
    literal_param_v = random.choice(parametr_values)
    relation= random.choice(relations)

    return {
        'param': literal_param_v.param.id,
        'value': literal_param_v.value,
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

    p = Parameter(system=es, name="Цвета")
    p.save()

    q = Question(system=es, body="Ваш любимые цвета?", type=Question.SELECT, parameter=p)
    q.save()

    pv = ParameterValue(system=es, param=p, value="холодные")
    pv.save()
    parametr_values.append(pv)

    answer = Answer(body="Холодные", question=q, parameter_value=pv)
    answer.save()

    pv = ParameterValue(system=es, param=p, value="Теплые")
    pv.save()
    parametr_values.append(pv)

    answer = Answer(body="Теплые", question=q, parameter_value=pv)
    answer.save()


def insert_objects():
    es = System.objects.first()
    object = SysObject(name="Курица", system=es)
    object.save()
    add_object_attribute(object)

    object = SysObject(name="Собака", system=es)
    object.save()
    add_object_attribute(object)

    object = SysObject(name="Кошка", system=es)
    object.save()
    add_object_attribute(object)


def add_object_attribute(object):
    for x in xrange(random.randint(1,4)):
        object.attributes.add(random.choice(attributes_values))


def run():
    clear_db()
    insert_es()
    insert_parameters()
    insert_attr()
    insert_rules()
    insert_objects()