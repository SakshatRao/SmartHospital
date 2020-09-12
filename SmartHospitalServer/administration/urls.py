from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path
from . import views

app_name = 'administration'

urlpatterns = [
    re_path(r'^$', views.homepage_view, name = 'homepage'),
    re_path(r'^stats/$', views.stats_view, name = 'stats'),
]