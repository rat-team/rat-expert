from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

from django.contrib import admin
from ExpertSystem.redact.attributes import add_attributes, insert_attributes, delete_attribute_value, delete_attribute
from ExpertSystem.redact.parameters import add_parameters
from ExpertSystem.redact.system import create_db, add_system, insert_system
from ExpertSystem.views import index
from ExpertSystem.views import answer
from ExpertSystem.views import reset

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ES.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^create/', create_db),
    url(r'^reset', reset, name="reset"),

    url(r'^index$', index, name="index"),
    url(r'^$', index, name="index"),
    url(r'^answer/$', answer, name="answer"),

    url(r'^add_system/(?P<system_id>[a-zA-Z0-9._-]+)/$', add_system, name="add_system"),
    url(r'^add_system/$', add_system, name="add_system"),
    url(r'^add_attributes$', add_attributes, name="add_attributes"),
    url(r'^add_parameters', add_parameters, name="add_parameters"),

    url(r'^insert_system/$', insert_system, name="insert_system"),
    url(r'^insert_attributes/$', insert_attributes, name="insert_attributes"),
    url(r'^delete_attribute_value/$',delete_attribute_value, name="delete_attribute_value"),
    url(r'^delete_attribute/$',delete_attribute, name="delete_attribute"),


)
