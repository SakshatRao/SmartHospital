from django.db import models
from accounts.models import Patient

# Create your models here.

# Health Status:
#   1. Temperature
#   2. SpO2
#   3. BPM
class Health_Status(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    temperature = models.DecimalField(max_digits = 5, decimal_places = 3)
    spO2 = models.DecimalField(max_digits = 5, decimal_places = 2)
    bpm = models.DecimalField(max_digits = 5, decimal_places = 2)
    recorded_time = models.DateTimeField(auto_now_add = True)