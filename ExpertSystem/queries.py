from ES.settings import QUERIES_DEBUG
from ExpertSystem.models import AttributeValue, Attribute


def add_weight_to_objects(objects, attribute_id, values_ids):

    all_attr_values = AttributeValue.objects.filter(attr__id=attribute_id, id__in=values_ids)
    base_weight = 0
    if len(all_attr_values) != 0:
        base_weight = 1 / float(len(all_attr_values))

    if QUERIES_DEBUG:
        print ("Attribute " + str(Attribute.objects.get(attribute_id)) + ". Base weight " + str(base_weight))
    obj_weight = 0
    for obj in objects:
        for attr_value in all_attr_values:
            if attr_value.sys_objects.filter(name=obj):
                obj_weight += 1
        objects[obj] += base_weight * obj_weight
        if QUERIES_DEBUG:
            print (str(obj) + ". Object weight " + str(obj_weight))
        obj_weight = 0


def update_session_attributes(session, attributes):
    for obj in session['objects']:
        session['objects'][obj] = 0
    for attr in attributes:
        add_weight_to_objects(session['objects'], attr, attributes[attr])
    return session
