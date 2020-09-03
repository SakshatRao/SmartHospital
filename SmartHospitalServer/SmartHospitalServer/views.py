from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def is_patient(request):
    try:
        is_patient = request.user.patient
        return True
    except:
        return False

def homepage_view(request):
    return render(request, 'homepage.html', {'is_patient': is_patient(request)})

def about_view(request):
    return render(request, 'about.html', {'is_patient': is_patient(request)})

def features_view(request):
    return render(request, 'features.html', {'is_patient': is_patient(request)})

def contact_view(request):
    return render(request, 'contact.html', {'is_patient': is_patient(request)})

def unauthorized_view(request):
    return render(request, 'unauthorized.html', {'is_patient': is_patient(request)})