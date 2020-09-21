from django.db import models
from accounts.models import Patient

# Create your models here.
class Patient_Health(models.Model):
    patient = models.OneToOneField(Patient, on_delete = models.CASCADE)
    temperature = models.DecimalField(max_digits = 5, decimal_places = 3)
    recorded_time = models.DateTimeField(auto_now_add = True)