from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^create$', views.create, name='create'),
  url(r'^put-your-cheat-code-here$', views.all, name='all'),
  url(r'^(?P<key>[0-9a-z]+)$', views.play, name='play')
]
