from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path
from . import views

app_name = 'staff'

urlpatterns = [
    re_path(r'^$', views.homepage_view, name = 'homepage'),
    re_path(r'^validate_patient/$', views.validate_patient, name = 'validate_patient'),
    re_path(r'^remove_patient/$', views.remove_patient, name = 'remove_patient'),
    re_path(r'^view_health_status/$', views.view_health_status, name = 'view_health_status'),
    re_path(r'^view_indiv_health_status/$', views.view_indiv_health_status, name = 'view_indiv_health_status'),
    re_path(r'^temperature_graph/$', views.temperature_graph_view, name = 'temperature_graph'),
]