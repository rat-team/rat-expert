from django.conf.urls import patterns, include, url

from django.contrib import admin
from ExpertSystem.views import index, create_db

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ES.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^create/', create_db),
    url(r'^index$', index, "index"),
    url(r'^$', index, name="index"),
)
