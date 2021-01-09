from django.db import models
from accounts.models import Patient, All_Patient, All_Staff

# Create your models here.

# Prescription: When doctors have prescribed medication
#   > Helps in convenient and remote digital access
#   > Can easily be shared with relevant people
#   > Avoids inconveniences caused due to handwriting, etc.
class Prescription_entry(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.SET_NULL, default = 1, null = True, limit_choices_to = {'is_validated': True})
    all_patient = models.ForeignKey(All_Patient, on_delete = models.CASCADE, default = '')
    staff = models.ForeignKey(All_Staff, on_delete = models.CASCADE, default = 1)
    medication = models.CharField(max_length = 50)
    instruction = models.TextField(max_length = 200)
    date = models.DateField(auto_now = True)

    def __str__(self):
        return self.medication

# Bill: When hospital is charging patients for a service
#   > Helps patients understand and analyze the hospital charges
#   > Can serve to validate hospital's income
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

# Medical History: When a patient has undergone a medical treatment
#   > Helps avoid medical issues related to a patient's earlier treatment before the current treatment
#   > Helps patients remember all medical events
class MedHistory_entry(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.SET_NULL, default = 1, null = True, limit_choices_to = {'is_validated': True})
    all_patient = models.ForeignKey(All_Patient, on_delete = models.CASCADE, default = '')
    staff = models.ForeignKey(All_Staff, on_delete = models.CASCADE, default = 1)
    event = models.CharField(max_length = 50)
    details = models.TextField(max_length = 200)
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.event