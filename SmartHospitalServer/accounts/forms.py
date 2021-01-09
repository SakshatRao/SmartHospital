from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

# Variables fixed for all users
class User_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

# Variables specific to staff
class Staff_Form(forms.ModelForm):
    class Meta:
        model = models.Staff
        fields = ['DOB', 'age', 'gender', 'contact', 'street_address', 'pin_code', 'occupation']
        widgets = {
            'DOB': forms.DateInput(attrs = {'type': 'date'})
        }

# Variables specific to patients
class Patient_Form(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = ['DOB', 'age', 'gender', 'contact', 'street_address', 'pin_code', 'blood_type', 'room_number']
        widgets = {
            'DOB': forms.DateInput(attrs = {'type': 'date'})
        }