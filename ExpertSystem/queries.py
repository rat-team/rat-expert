import MySQLdb
from ES.settings import DATABASES
from ExpertSystem.models import SysObject, AttributeValue


def add_weight_to_objects(objects, attribute, values):

    all_attr_values = AttributeValue.objects.filter(attr__name=attribute, value__in=values)
    base_weight = 0
    if len(all_attr_values) != 0:
        base_weight = 1 / float(len(all_attr_values))

    obj_weight = 0
    for obj in objects:
        for attr_value in all_attr_values:
            if attr_value.sysobject_set.filter(name=obj):
                obj_weight += 1
        objects[obj] += base_weight * obj_weight
        obj_weight = 0