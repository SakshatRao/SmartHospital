from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

# Staff: Current staff users
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    staff_email = models.EmailField(default = '', unique = True)
    DOB = models.DateField(verbose_name = 'Birth Date')
    age = models.IntegerField()
    gender = models.CharField(choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default = 'M', max_length = 50)
    contact = models.CharField(max_length = 10, default = '')
    street_address = models.TextField(max_length = 200, default = '')
    pin_code = models.CharField(max_length = 6, default = '')
    occupation = models.CharField(choices = [('D', 'Doctor'), ('N', 'Nurse')], default = 'D', max_length = 20)
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

# Patient: Current patient users
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    patient_email = models.EmailField(default = '', unique = True)
    DOB = models.DateField(verbose_name = 'Birth Date')
    age = models.IntegerField()
    gender = models.CharField(choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default = 'M', max_length = 50)
    contact = models.CharField(max_length = 10, default = '')
    street_address = models.TextField(max_length = 200, default = '')
    pin_code = models.CharField(max_length = 6, default = '')
    blood_type = models.CharField(choices = [(x, x) for x in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']], default = 'A+', max_length = 5)
    room_number = models.IntegerField(null = True, blank = True, unique = True)
    is_validated = models.BooleanField(default = False)
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

# All_Staff: All existing (active/inactive) staff users
class All_Staff(models.Model):
    staff = models.OneToOneField(Staff, on_delete = models.SET_NULL, null = True)
    staff_name = models.CharField(max_length = 50, default = '')
    staff_email = models.EmailField(default = '', unique = True)
    creation_date = models.DateField(auto_now_add = True)
    def __str__(self):
        return self.staff_name

# All_Patient: All existing (active/inactive) patient users
class All_Patient(models.Model):
    patient = models.OneToOneField(Patient, on_delete = models.SET_NULL, null = True)
    patient_name = models.CharField(max_length = 50, default = '')
    patient_email = models.EmailField(default = '', unique = True)
    creation_date = models.DateField(auto_now_add = True)
    admission_date = models.DateField(null = True, blank = True)
    discharge_date = models.DateField(null = True, blank = True)
    def __str__(self):
        return self.patient_name