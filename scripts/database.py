# coding=utf-8

from ExpertSystem.models import Question, System, Parameter, ParameterValue

__author__ = 'maxim'


def insert_es():
    es = System(name="Экспертная система по выбору дерьма")
    es.save()

def insert_parameters():
    es = System.objects.first()

    p = Parameter(system=es, name="Нос")
    p.save()
    q = Question(system=es, body="Что вы любите есть?", type=Question.SELECT, parameter=p)
    q.save()
    pv = ParameterValue(system=es, param=p, value="В говне")
    pv.save()
    pv = ParameterValue(system=es, param=p, value="Чистый")
    pv.save()
    pv = ParameterValue(system=es, param=p, value="Отрезанный")
    pv.save()

    p = Parameter(system=es, name="Усы")
    p.save()
    q = Question(system=es, body="Что вы любите пить?", type=Question.SELECT, parameter=p)
    q.save()
    pv = ParameterValue(system=es, param=p, value="Длинные")
    pv.save()
    pv = ParameterValue(system=es, param=p, value="Обпаленные")
    pv.save()
    pv = ParameterValue(system=es, param=p, value="Прореженные лишаем")
    pv.save()

    p = Parameter(system=es, name="Хвост")
    p.save()
    q = Question(system=es, body="Что вы любите бить?", type=Question.SELECT, parameter=p)
    q.save()
    pv = ParameterValue(system=es, param=p, value="Длинные")
    pv.save()
    pv = ParameterValue(system=es, param=p, value="Обрубили каблуком")
    pv.save()


def run():
    insert_es()
    insert_parameters()