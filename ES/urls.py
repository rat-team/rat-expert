from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ES import settings
from ES.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from ExpertSystem.redact.answers import add_answers, insert_answers, delete_answer
from ExpertSystem.redact.attributes import add_attributes, insert_attributes, delete_attribute_value, delete_attribute
from ExpertSystem.redact.objects import add_objects, insert_objects
from ExpertSystem.redact.parameters import add_parameters, insert_parameters, delete_parameter
from ExpertSystem.redact.questions import add_questions, insert_questions, delete_question
from ExpertSystem.redact.rules import add_rules, insert_rules
from ExpertSystem.redact.system import create_db, add_system, insert_system
from ExpertSystem.views import index, login_view, registration, creators, answer, reset, logout_view, main_menu, \
    skip_question, presentation, delete_system, faq

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ES.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^create/', create_db),
    url(r'^reset', reset, name="reset"),

    url(r'^$', index, name="index"),
    url(r'^index/$', index, name="index"),
    url(r'^main/$', main_menu, name="main_menu"),
    url(r'^presentation/$', presentation, name="presentation"),
    url(r'^faq/$', faq, name="faq"),
    url(r'^skip/(?P<question_id>[0-9]+)/$', skip_question, name="skip_question"),


    url(r'^creators/$', creators, name="creators"),
    url(r'^answer/$', answer, name="answer"),

    url(r'^login/$', login_view, name="login_view"),
    url(r'^registration/$', registration, name="registration"),
    url(r'^logout/$', logout_view, name="logout_view"),

    url(r'^add_system/(?P<system_id>[a-zA-Z0-9._-]+)/$', add_system, name="add_system"),
    url(r'^add_system/$', add_system, name="add_system"),
    url(r'^add_attributes$', add_attributes, name="add_attributes"),
    url(r'^add_parameters$', add_parameters, name="add_parameters"),
    url(r'^add_objects$', add_objects, name="add_objects"),
    url(r'^add_answers$', add_answers, name="add_answers"),
    url(r'^add_questions$', add_questions, name="add_questions"),
    url(r'^add_rules$', add_rules, name="add_rules"),

    url(r'^insert_system/$', insert_system, name="insert_system"),
    url(r'^insert_attributes/$', insert_attributes, name="insert_attributes"),
    url(r'^insert_parameters/$', insert_parameters, name="insert_parameters"),
    url(r'^insert_objects/$', insert_objects, name="insert_objects"),
    url(r'^insert_answers/$', insert_answers, name="insert_answers"),
    url(r'^insert_questions/$', insert_questions, name="insert_questions"),
    url(r'^insert_rules/$', insert_rules, name="insert_rules"),


    # url(r'^insert_objects/$', insert_objects, name="insert_objects"),
    url(r'^delete_attribute_value/$', delete_attribute_value, name="delete_attribute_value"),
    url(r'^delete_attribute/$', delete_attribute, name="delete_attribute"),
    url(r'^delete_parameter/$', delete_parameter, name="delete_parameter"),
    url(r'^delete_answer/$', delete_answer, name="delete_answer"),
    url(r'^delete_question/$', delete_question, name="delete_question"),
    url(r'^delete_system/(?P<system_id>[a-zA-Z0-9._-]+)/$', delete_system, name="delete_system")

)

if DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': MEDIA_ROOT}))

    urlpatterns += static(MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()
