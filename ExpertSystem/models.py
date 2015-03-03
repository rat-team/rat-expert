# coding=utf-8
from django.db import models


class System(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table="system"


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    system = models.ForeignKey(System)

    class Meta:
        db_table="attribute"


class Parameter(models.Model):
    name = models.CharField(max_length=50)
    system = models.ForeignKey(System)

    class Meta:
        db_table="parameter"


class Question(models.Model):
    SELECT = 0
    NUMBER = 1
    CHOISES = (
        (SELECT, "Выберите ответ"),
        (NUMBER, "Напишите число"),
    )
    #Атрибут, к которому привязан вопрос
    parameter = models.ForeignKey(Attribute)
    body = models.TextField()
    system = models.ForeignKey(System)
    type = models.IntegerField(choices=CHOISES)

    class Meta:
        db_table="question"


class Answer(models.Model):
    question = models.ForeignKey(Question)
    body = models.TextField()
    parameter_value = models.ForeignKey(ParameterValue)

    class Meta:
        db_table="answer"


class ParameterValue(models.Model):
    system = models.ForeignKey(System)
    param = models.ForeignKey(Parameter)
    value = models.CharField(max_length=50)

    class Meta:
        db_table="parameter_value"


class AttributeValue(models.Model):
    system = models.ForeignKey(System)
    attr = models.ForeignKey(Attribute)
    value = models.CharField(max_length=50)

    class Meta:
        db_table="attrubite_value"


class SysObject(models.Model):
    name = models
    #Список атрибутов и их значений у объекта
    attributes = models.ManyToManyField(AttributeValue)

    class Meta:
        db_table="sys_object"


class Rule(models.Model):
    PARAM_RULE = 0
    ATTR_RULE = 1
    CHOISES = (
        (PARAM_RULE, "Правило для параметра"),
        (ATTR_RULE, "Правило для атрибута"),
    )
    condition = models.TextField()
    result = models.TextField()
    type = models.IntegerField(choices=CHOISES)

    class Meta:
        db_table="rule"

