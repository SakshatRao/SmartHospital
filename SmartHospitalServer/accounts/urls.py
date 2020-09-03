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
]