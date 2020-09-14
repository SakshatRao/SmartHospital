from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, decorators
from django.db import IntegrityError

import datetime

from . import forms
from .models import Staff, Patient, All_Staff, All_Patient
from utils.access import http_dict_func, patient_access, staff_access

# Create your views here.
def signup_staff_view(request):
    if(request.method == 'POST'):
        user_form = forms.User_Form(request.POST)
        staff_form = forms.Staff_Form(request.POST)
        if(user_form.is_valid() & staff_form.is_valid()):
            user = user_form.save()
            staff = staff_form.save(commit = False)
            staff.user = user
            staff.staff_email = user.email
            staff.is_validated = False
            try:
                staff.save()
                login(request, user)
                existing_staff = All_Staff.objects.filter(staff_email = user.email)
                if(len(existing_staff) == 0):
                    new_staff = All_Staff()
                    new_staff.staff_email = user.email
                else:
                    new_staff = existing_staff[0]
                new_staff.staff_name = user.first_name + ' ' + user.last_name
                new_staff.save()
                return redirect('staff:homepage')
            except IntegrityError:
                user.delete()
                return render(request, 'already_exists.html', http_dict_func(request))
    else:
        user_form = forms.User_Form()
        staff_form = forms.Staff_Form()
    http_dict = http_dict_func(request)
    http_dict['user_form'] = user_form
    http_dict['staff_form'] = staff_form
    return render(request, 'accounts/signup_staff.html', http_dict)

def signup_patient_view(request):
    if(request.method == 'POST'):
        user_form = forms.User_Form(request.POST)
        patient_form = forms.Patient_Form(request.POST)
        if(user_form.is_valid() & patient_form.is_valid()):
            user = user_form.save()
            patient = patient_form.save(commit = False)
            patient.user = user
            patient.patient_name = user.first_name + ' ' + user.last_name
            patient.patient_email = user.email
            patient.is_validated = False
            try:
                patient.save()
                login(request, user)
                existing_patient = All_Patient.objects.filter(patient_email = user.email)
                if(len(existing_patient) == 0):
                    new_patient = All_Patient()
                    new_patient.patient_email = user.email
                else:
                    new_patient = existing_patient[0]
                new_patient.admission_date = datetime.date.today()
                new_patient.discharge_date = None
                new_patient.patient_name = user.first_name + ' ' + user.last_name
                new_patient.save()
                return redirect('patient:homepage')
            except IntegrityError:
                user.delete()
                return render(request, 'already_exists.html', http_dict_func(request))
    else:
        user_form = forms.User_Form()
        patient_form = forms.Patient_Form()
    http_dict = http_dict_func(request)
    http_dict['user_form'] = user_form
    http_dict['patient_form'] = patient_form
    return render(request, 'accounts/signup_patient.html', http_dict)

def login_view(request):
    if(request.method == 'POST'):
        user_form = AuthenticationForm(data = request.POST)
        if(user_form.is_valid()):
            user = user_form.get_user()
            login(request, user)
            if('next' in request.POST):
                return redirect(request.POST.get('next'))
            else:
                if(user.is_superuser):
                    return redirect('administration:homepage')
                else:
                    try:
                        _ = user.patient
                        return redirect('patient:homepage')
                    except:
                        return redirect('staff:homepage')
    else:
        user_form = AuthenticationForm()
    http_dict = http_dict_func(request)
    http_dict['user_form'] = user_form
    return render(request, 'accounts/login.html', http_dict)

@decorators.login_required(login_url = 'homepage')
def logout_view(request):
    assert request.method == 'POST'
    logout(request)
    return redirect('homepage')

@patient_access()
def edit_patient(request):
    if(request.method == 'POST'):
        user_form = forms.User_Form(request.POST, instance = request.user)
        patient_form = forms.Patient_Form(request.POST, instance = request.user.patient)
        if(user_form.is_valid() & patient_form.is_valid()):
            user = user_form.save()
            patient = patient_form.save(commit = False)
            patient.user = user
            patient.save()
            login(request, user)
            return redirect('patient:homepage')
    else:
        user_form = forms.User_Form(instance = request.user)
        patient_form = forms.Patient_Form(instance = request.user.patient)
    http_dict = http_dict_func(request)
    http_dict['user_form'] = user_form
    http_dict['patient_form'] = patient_form
    return render(request, 'accounts/edit_patient.html', http_dict)

@staff_access()
def edit_staff(request):
    if(request.method == 'POST'):
        user_form = forms.User_Form(request.POST, instance = request.user)
        staff_form = forms.Staff_Form(request.POST, instance = request.user.staff)
        if(user_form.is_valid() & staff_form.is_valid()):
            user = user_form.save()
            staff = staff_form.save(commit = False)
            staff.user = user
            staff.save()
            login(request, user)
            return redirect('staff:homepage')
    else:
        user_form = forms.User_Form(instance = request.user)
        staff_form = forms.Staff_Form(instance = request.user.staff)
    http_dict = http_dict_func(request)
    http_dict['user_form'] = user_form
    http_dict['staff_form'] = staff_form
    return render(request, 'accounts/edit_staff.html', http_dict)