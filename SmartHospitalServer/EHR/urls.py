from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path
from . import views

app_name = 'ehr'

urlpatterns = [
    re_path(r'^add-entry/$', views.add_entry_view, name = 'add-entry'),
    re_path(r'^view-ehr/$', views.view_ehr_view, name = 'view-ehr')
]