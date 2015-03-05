from django.contrib import admin

# Register your models here.
from ExpertSystem.models import *

admin.site.register(System)
admin.site.register(Attribute)
admin.site.register(Parameter)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ParameterValue)
admin.site.register(AttributeValue)
admin.site.register(SysObject)
admin.site.register(Rule)
