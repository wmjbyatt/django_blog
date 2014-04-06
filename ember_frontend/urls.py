from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from ember_frontend import views

urlpatterns = patterns('',
  url(r'^$', views.main_page),
)
