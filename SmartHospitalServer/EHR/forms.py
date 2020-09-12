from django import forms
from . import models

class Prescription_entry_Form(forms.ModelForm):
    class Meta:
        model = models.Prescription_entry
        fields = ['patient', 'medication', 'instruction']
        widgets = {
            'patient': forms.Select()
        }

class Bill_entry_Form(forms.ModelForm):
    class Meta:
        model = models.Bill_entry
        fields = ['patient', 'service', 'details', 'charge']
        widgets = {
            'patient': forms.Select()
        }

class MedHistory_entry_Form(forms.ModelForm):
    class Meta:
        model = models.MedHistory_entry
        fields = ['patient', 'event', 'details']
        widgets = {
            'patient': forms.Select()
        }