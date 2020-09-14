from django.contrib import admin
from .models import Staff, Patient, All_Staff, All_Patient

# Register your models here.
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(All_Staff)
admin.site.register(All_Patient)