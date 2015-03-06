from django.conf.urls import patterns, include, url

from django.contrib import admin
from ExpertSystem.views import index, create_db, answer, add_system

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ES.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^create/', create_db),

    url(r'^index$', index, name="index"),
    url(r'^$', index, name="index"),
    
    url(r'^add_system/(?P<page>\d+)$', add_system, name="index"),

    url(r'^answer/$', answer, name="answer"),

)
