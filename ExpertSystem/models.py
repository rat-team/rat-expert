# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class System(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "system"


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    system = models.ForeignKey(System)

    class Meta:
        db_table = "attribute"

    def __unicode__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(max_length=50)
    system = models.ForeignKey(System)

    class Meta:
        db_table = "parameter"


class Question(models.Model):
    SELECT = 0
    NUMBER = 1
    CHOICES = (
        (SELECT, "Выберите ответ"),
        (NUMBER, "Напишите число"),
    )
    # Параметр, к которому привязан вопрос
    parameter = models.ForeignKey(Parameter)
    body = models.TextField()
    system = models.ForeignKey(System)
    type = models.IntegerField(choices=CHOICES)

    class Meta:
        db_table = "question"


class ParameterValue(models.Model):
    system = models.ForeignKey(System)
    param = models.ForeignKey(Parameter)
    value = models.CharField(max_length=50)

    class Meta:
        db_table = "parameter_value"


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers')
    body = models.TextField()
    parameter_value = models.TextField()

    class Meta:
        db_table = "answer"


class AttributeValue(models.Model):
    system = models.ForeignKey(System)
    attr = models.ForeignKey(Attribute, on_delete=CASCADE)
    value = models.CharField(max_length=50)

    class Meta:
        db_table = "attribute_value"

    def __unicode__(self):
        return str(self.id) + ". " + self.attr.name + " : " + self.value


class SysObject(models.Model):
    name = models.TextField()
    #Список атрибутов и их значений у объекта
    attributes = models.ManyToManyField(AttributeValue, null=True, blank=True, related_name='sys_objects')
    system = models.ForeignKey(System)

    class Meta:
        db_table = "sys_object"

    def __unicode__(self):
        return self.name


class Rule(models.Model):
    PARAM_RULE = 0
    ATTR_RULE = 1
    CHOICES = (
        (PARAM_RULE, "Правило для параметра"),
        (ATTR_RULE, "Правило для атрибута"),
    )
    condition = models.TextField()
    result = models.TextField()
    type = models.IntegerField(choices=CHOICES)
    system = models.ForeignKey(System)

    class Meta:
        db_table = "rule"

