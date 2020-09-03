from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

class User_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class Staff_Form(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = ['DOB', 'age', 'occupation']
        widgets = {
            'DOB': forms.DateInput(attrs = {'type': 'date'})
        }

class Patient_Form(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = ['DOB', 'age', 'blood_type', 'contact', 'address']
        widgets = {
            'DOB': forms.DateInput(attrs = {'type': 'date'})
        }