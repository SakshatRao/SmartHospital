from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import Staff
from . import forms

# Create your views here.
def signup_staff_view(request):
    if(request.method == 'POST'):
        user_form = forms.User_Form(request.POST)
        staff_form = forms.Staff_Form(request.POST)
        if(user_form.is_valid() & staff_form.is_valid()):
            user = user_form.save()
            staff = staff_form.save(commit = False)
            staff.user = user
            staff.save()
            login(request, user)
            return redirect('staff:homepage')
    else:
        user_form = forms.User_Form()
        staff_form = forms.Staff_Form()
    return render(request, 'accounts/signup_staff.html', {'user_form': user_form, 'staff_form': staff_form})

def signup_patient_view(request):
    if(request.method == 'POST'):
        user_form = forms.User_Form(request.POST)
        patient_form = forms.Patient_Form(request.POST)
        if(user_form.is_valid() & patient_form.is_valid()):
            user = user_form.save()
            patient = patient_form.save(commit = False)
            patient.user = user
            patient.save()
            login(request, user)
            return redirect('patient:homepage')
    else:
        user_form = forms.User_Form()
        patient_form = forms.Patient_Form()
    return render(request, 'accounts/signup_patient.html', {'user_form': user_form, 'patient_form': patient_form})

def login_view(request):
    if(request.method == 'POST'):
        user_form = AuthenticationForm(data = request.POST)
        if(user_form.is_valid()):
            user = user_form.get_user()
            login(request, user)
            if('next' in request.POST):
                return redirect(request.POST.get('next'))
            else:
                try:
                    is_patient = user.patient
                    return redirect('patient:homepage')
                except:
                    return redirect('staff:homepage')
    else:
        user_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'user_form': user_form})

def logout_view(request):
    assert request.method == 'POST'
    logout(request)
    return redirect('homepage')