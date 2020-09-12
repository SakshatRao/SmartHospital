from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^signup_patient/$', views.signup_patient_view, name = 'signup_patient'),
    url(r'^signup_staff/$', views.signup_staff_view, name = 'signup_staff'),
    url(r'^login/$', views.login_view, name = 'login'),
    url(r'^logout/$', views.logout_view, name = 'logout'),
    url(r'^edit_patient/$', views.edit_patient, name = 'edit_patient'),
    url(r'^edit_staff/$', views.edit_staff, name = 'edit_staff'),
    url(r'^delete_patient/$', views.delete_patient, name = 'delete_patient'),
    url(r'^delete_staff/$', views.delete_staff, name = 'delete_staff'),
]