from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, decorators
from django.db import IntegrityError
from .models import Staff
from . import forms
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
            staff.staff_name = user.first_name + ' ' + user.last_name
            staff.staff_email = user.email
            try:
                staff.save()
                login(request, user)
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
            try:
                patient.save()
                login(request, user)
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

@patient_access()
def delete_patient(request):
    if(request.method == 'POST'):
        user_form = AuthenticationForm(data = request.POST)
        if(user_form.is_valid()):
            request.user.delete()
            return redirect('homepage')
    else:
        user_form = AuthenticationForm()
    http_dict = http_dict_func(request)
    http_dict['user_form'] = user_form
    return render(request, 'accounts/delete_patient.html', http_dict)

@staff_access()
def delete_staff(request):
    if(request.method == 'POST'):
        user_form = AuthenticationForm(data = request.POST)
        if(user_form.is_valid()):
            request.user.delete()
            return redirect('homepage')
    else:
        user_form = AuthenticationForm()
    http_dict = http_dict_func(request)
    http_dict['user_form'] = user_form
    return render(request, 'accounts/delete_staff.html', http_dict)