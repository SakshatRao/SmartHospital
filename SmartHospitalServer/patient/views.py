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

def patient_access():
    def check_patient(user):
        try:
            is_patient = user.patient
            return True
        except:
            return False
    return user_passes_test(check_patient, login_url='unauthorized')

@patient_access()
def homepage_view(request):
    return render(request, 'patient/homepage.html', {'is_patient': is_patient(request)})