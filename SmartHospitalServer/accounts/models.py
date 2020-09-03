from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    DOB = models.DateField(verbose_name = 'Birth Date')
    age = models.IntegerField()
    occupation = models.CharField(choices = [('D', 'Doctor'), ('N', 'Nurse')], default = 'N', max_length = 20)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Patient(models.Model):

    class Meta:
        permissions = [
            ('patient_access', 'Access for Patients'),
        ]

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    DOB = models.DateField(verbose_name = 'Birth Date')
    age = models.IntegerField()
    blood_type = models.CharField(choices = [(x, x) for x in ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']], default = 'A+', max_length = 5)
    contact = models.CharField(max_length = 10)
    address = models.TextField(max_length = 200)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name