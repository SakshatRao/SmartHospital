from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from utils.access import http_dict_func, admin_access

from accounts.models import Patient, Staff
from EHR.models import Bill_entry
from plotly_graphs import stats

@admin_access()
def homepage_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'administration/homepage.html', http_dict)

@admin_access()
def stats_view(request):
    patient_db = Patient.objects.all()
    staff_db = Staff.objects.all()
    bill_db = Bill_entry.objects.all()
    
    stats.room_occupancy(patient_db)
    stats.monthly_billing(bill_db)
    stats.gender_ratio(staff_db)
    stats.daily_billing(bill_db)
    stats.patient_geomap(patient_db)
    stats.age_histogram(patient_db)

    http_dict = http_dict_func(request)
    return render(request, 'administration/stats.html', http_dict)