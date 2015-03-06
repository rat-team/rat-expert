from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

from django.contrib import admin
from ExpertSystem.views import index
from ExpertSystem.views import create_db
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

)
