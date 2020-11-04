from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'^signup_patient/$', views.signup_patient_view, name = 'signup_patient'),
    re_path(r'^signup_staff/$', views.signup_staff_view, name = 'signup_staff'),
    re_path(r'^login/$', views.login_view, name = 'login'),
    re_path(r'^logout/$', views.logout_view, name = 'logout'),
    re_path(r'^edit_patient/$', views.edit_patient, name = 'edit_patient'),
    re_path(r'^edit_staff/$', views.edit_staff, name = 'edit_staff'),
]