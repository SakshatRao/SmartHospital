from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from utils.access import http_dict_func

def homepage_view(request):
    return render(request, 'homepage.html', http_dict_func(request))

def about_view(request):
    return render(request, 'about.html', http_dict_func(request))

def features_view(request):
    return render(request, 'features.html', http_dict_func(request))

def contact_view(request):
    return render(request, 'contact.html', http_dict_func(request))

def unauthorized_view(request):
    return render(request, 'unauthorized.html', http_dict_func(request))