from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from utils.access import patient_access, is_patient

def http_dict_func(request):
    return {'is_patient': is_patient(request)}

@patient_access()
def homepage_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'patient/homepage.html', http_dict)