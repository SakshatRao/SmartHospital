from django.db import models
from accounts.models import Patient, All_Patient, All_Staff

# Create your models here.
class Prescription_entry(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.SET_NULL, default = 1, null = True, limit_choices_to = {'is_validated': True})
    all_patient = models.ForeignKey(All_Patient, on_delete = models.CASCADE, default = '')
    staff = models.ForeignKey(All_Staff, on_delete = models.CASCADE, default = 1)
    medication = models.CharField(max_length = 50)
    instruction = models.TextField(max_length = 200)
    date = models.DateField(auto_now = True)

    def __str__(self):
        return self.medication
    
class Bill_entry(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.SET_NULL, default = 1, null = True, limit_choices_to = {'is_validated': True})
    all_patient = models.ForeignKey(All_Patient, on_delete = models.CASCADE, default = '')
    staff = models.ForeignKey(All_Staff, on_delete = models.CASCADE, default = 1)
    service = models.CharField(max_length = 50)
    details = models.TextField(max_length = 200)
    charge = models.DecimalField(max_digits = 10, decimal_places = 2)
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.service

class MedHistory_entry(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.SET_NULL, default = 1, null = True, limit_choices_to = {'is_validated': True})
    all_patient = models.ForeignKey(All_Patient, on_delete = models.CASCADE, default = '')
    staff = models.ForeignKey(All_Staff, on_delete = models.CASCADE, default = 1)
    event = models.CharField(max_length = 50)
    details = models.TextField(max_length = 200)
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.event