from django.contrib import admin
from django.conf.urls import include
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.homepage_view, name = 'homepage'),
    re_path(r'^about/$', views.about_view, name = 'about'),
    re_path(r'^features/$', views.features_view, name = 'features'),
    re_path(r'^contact/$', views.contact_view, name = 'contact'),
    re_path(r'^unauthorized/$', views.unauthorized_view, name = 'unauthorized'),
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^patient/', include('patient.urls')),
    re_path(r'^staff/', include('staff.urls')),
]