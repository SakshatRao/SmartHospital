from django.contrib import admin
from .models import Prescription_entry, Bill_entry, MedHistory_entry

# Register your models here.
admin.site.register(Prescription_entry)
admin.site.register(Bill_entry)
admin.site.register(MedHistory_entry)