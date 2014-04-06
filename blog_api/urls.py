from django.conf.urls import patterns, url, include
from blog_api import views

urlpatterns = patterns('',
  url(r'^users/(?P<pk>\d+)/$', views.UserView.as_view()),
  url(r'^users/$', views.UsersView.as_view()),
  
  url(r'^posts/(?P<pk>\d+)/$', views.PostView.as_view()),
  url(r'^posts/$', views.PostsView.as_view()),
  
  url(r'^session/$', views.SessionView.as_view()),
  
  # Lets us log in to the browseable API
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
