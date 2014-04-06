from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
  url(r'^api/', include('blog_api.urls')),
  url(r'^', include('ember_frontend.urls')),
)
