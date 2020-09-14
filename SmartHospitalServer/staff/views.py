from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from utils.access import http_dict_func, staff_access
from accounts.models import Patient, All_Patient
from django.contrib.auth.models import User

import datetime

@staff_access()
def homepage_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'staff/homepage.html', http_dict)

@staff_access()
def validate_patient(request):
    if(request.method == 'POST'):
        for key in request.POST:
            if(key != 'csrfmiddlewaretoken'):
                valid_user = User.objects.get(username = key)
                valid_user.patient.is_validated = True
                valid_all_patient = All_Patient.objects.get(patient_email = valid_user.email)
                valid_all_patient.patient = valid_user.patient
                valid_user.patient.save()
                valid_all_patient.save()
        return redirect('staff:homepage')
    else:
        patients = Patient.objects.all()
        unvalidated_patients = []
        for patient in patients:
            try:
                _ = patient.all_patient
            except:
                unvalidated_patients.append(patient)
        http_dict = http_dict_func(request)
        http_dict['unvalid_patients'] = unvalidated_patients
        return render(request, 'staff/validate_patient.html', http_dict)

@staff_access()
def remove_patient(request):
    if(request.method == 'POST'):
        for key in request.POST:
            if(key != 'csrfmiddlewaretoken'):
                valid_user = User.objects.get(username = key)
                valid_all_patient = All_Patient.objects.get(patient_email = valid_user.email)
                valid_all_patient.discharge_date = datetime.date.today()
                valid_all_patient.save()
                valid_user.delete()
        return redirect('staff:homepage')
    else:
        patients = Patient.objects.all()
        validated_patients = []
        for patient in patients:
            try:
                _ = patient.all_patient
                validated_patients.append(patient)
            except:
                pass
        http_dict = http_dict_func(request)
        http_dict['valid_patients'] = validated_patients
        return render(request, 'staff/remove_patient.html', http_dict)