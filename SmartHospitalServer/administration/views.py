from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from utils.access import http_dict_func, admin_access

import datetime

from django.contrib.auth.models import User
from accounts.models import Patient, Staff, All_Patient, All_Staff
from EHR.models import Bill_entry
from plotly_graphs import administration_stats as stats

# Admin Homepage (Requires admin login)
@admin_access()
def homepage_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'administration/homepage.html', http_dict)

# Administration Statistics (requires admin login)
@admin_access()
def stats_view(request):
    patient_db = Patient.objects.filter(is_validated = True)
    all_patient_db = All_Patient.objects.all()
    staff_db = Staff.objects.all()
    bill_db = Bill_entry.objects.all()
    
    stats.room_occupancy(patient_db)
    stats.monthly_billing(bill_db)
    stats.gender_ratio(staff_db)
    stats.daily_billing(bill_db)
    stats.patient_geomap(patient_db)
    stats.age_histogram(patient_db)
    stats.admission_discharge_rate(all_patient_db)

    http_dict = http_dict_func(request)
    return render(request, 'administration/stats.html', http_dict)

# Validation of Staff (requires admin login)
@admin_access()
def validate_staff(request):
    if(request.method == 'POST'):
        for key in request.POST:
            if(key != 'csrfmiddlewaretoken'):
                valid_user = User.objects.get(username = key)
                valid_user.staff.is_validated = True
                valid_all_staff = All_Staff.objects.get(staff_email = valid_user.email)
                valid_all_staff.staff = valid_user.staff
                valid_user.staff.save()
                valid_all_staff.save()
        return redirect('administration:homepage')
    else:
        staffs = Staff.objects.all()
        unvalidated_staffs = []
        for staff in staffs:
            try:
                _ = staff.all_staff
            except:
                unvalidated_staffs.append(staff)
        http_dict = http_dict_func(request)
        http_dict['unvalid_staffs'] = unvalidated_staffs
        return render(request, 'administration/validate_staff.html', http_dict)

# Removal of Staff (requires admin login)
@admin_access()
def remove_staff(request):
    if(request.method == 'POST'):
        for key in request.POST:
            if(key != 'csrfmiddlewaretoken'):
                valid_user = User.objects.get(username = key)
                valid_all_staff = All_Staff.objects.get(staff_email = valid_user.email)
                valid_all_staff.discharge_date = datetime.date.today()
                valid_all_staff.save()
                valid_user.delete()
        return redirect('administration:homepage')
    else:
        staffs = Staff.objects.all()
        validated_staffs = []
        for staff in staffs:
            try:
                _ = staff.all_staff
                validated_staffs.append(staff)
            except:
                pass
        http_dict = http_dict_func(request)
        http_dict['valid_staffs'] = validated_staffs
        return render(request, 'administration/remove_staff.html', http_dict)