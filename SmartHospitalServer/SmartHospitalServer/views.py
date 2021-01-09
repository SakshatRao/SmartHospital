from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from utils.access import http_dict_func

# For viewing homepage
def homepage_view(request):
    return render(request, 'homepage.html', http_dict_func(request))

# For viewing About page
def about_view(request):
    return render(request, 'about.html', http_dict_func(request))

# For viewing Features page
def features_view(request):
    return render(request, 'features.html', http_dict_func(request))

# For viewing Contact page
def contact_view(request):
    return render(request, 'contact.html', http_dict_func(request))

# If unauthorization is detected
def unauthorized_view(request):
    return render(request, 'unauthorized.html', http_dict_func(request))