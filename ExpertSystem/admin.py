from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.db.models import get_models, get_model

admin.site.unregister(Group)
admin.site.unregister(User)
for model in get_models():
    admin.site.register(model)

