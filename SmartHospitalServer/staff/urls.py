from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path
from . import views

app_name = 'staff'

urlpatterns = [
    re_path(r'^$', views.homepage_view, name = 'homepage'),
    re_path(r'^validate_patient/$', views.validate_patient, name = 'validate_patient'),
    re_path(r'^remove_patient/$', views.remove_patient, name = 'remove_patient'),
]