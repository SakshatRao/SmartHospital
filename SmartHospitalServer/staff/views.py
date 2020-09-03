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

def staff_access():
    def check_staff(user):
        if(user.is_superuser):
            return True
        else:
            try:
                is_staff = user.staff
                return True
            except:
                return False
    return user_passes_test(check_staff, login_url='unauthorized')

@staff_access()
def homepage_view(request):
    return render(request, 'staff/homepage.html', {'is_patient': is_patient(request)})