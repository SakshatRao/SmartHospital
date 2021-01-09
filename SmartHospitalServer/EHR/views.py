from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .models import Prescription_entry, Bill_entry, MedHistory_entry
from utils.access import patient_access, staff_access, http_dict_func

# Create your views here.

# Page to add EHR entry (requires staff login)
@staff_access()
def add_entry_view(request):
    if(request.method == 'POST'):
        if('presc' in request.POST):
            presc_form = forms.Prescription_entry_Form(request.POST)
            if(presc_form.is_valid()):
                entry = presc_form.save(commit = False)
                entry.all_patient = entry.patient.all_patient
                entry.staff = request.user.staff.all_staff
                entry.save()
                return redirect('staff:homepage')
            else:
                bill_form = forms.Bill_entry_Form()
                medhist_form = forms.MedHistory_entry_Form()
        elif('bill' in request.POST):
            bill_form = forms.Bill_entry_Form(request.POST)
            if(bill_form.is_valid()):
                entry = bill_form.save(commit = False)
                entry.all_patient = entry.patient.all_patient
                entry.staff = request.user.staff.all_staff
                entry.save()
                return redirect('staff:homepage')
            else:
                presc_form = forms.Prescription_entry_Form()
                medhist_form = forms.MedHistory_entry_Form()
        elif('medhist' in request.POST):
            medhist_form = forms.MedHistory_entry_Form(request.POST)
            if(medhist_form.is_valid()):
                entry = medhist_form.save(commit = False)
                entry.all_patient = entry.patient.all_patient
                entry.staff = request.user.staff.all_staff
                entry.save()
                return redirect('staff:homepage')
            else:
                presc_form = forms.Prescription_entry_Form()
                bill_form = forms.Bill_entry_Form()
    else:
        presc_form = forms.Prescription_entry_Form()
        bill_form = forms.Bill_entry_Form()
        medhist_form = forms.MedHistory_entry_Form()
    http_dict = http_dict_func(request)
    http_dict['presc_form'] = presc_form
    http_dict['bill_form'] = bill_form
    http_dict['medhist_form'] = medhist_form
    return render(request, 'ehr/add_entry.html', http_dict)

# Page to view EHR contents (requires patient login)
@patient_access()
def view_ehr_view(request):
    presc_entries = list(request.user.patient.all_patient.prescription_entry_set.all().order_by('-date', 'medication'))
    bill_entries = list(request.user.patient.all_patient.bill_entry_set.all().order_by('-date', 'service'))
    medhist_entries = list(request.user.patient.all_patient.medhistory_entry_set.all().order_by('-date', 'event'))
    http_dict = http_dict_func(request)
    http_dict['presc_entries'] = presc_entries
    http_dict['bill_entries'] = bill_entries
    http_dict['medhist_entries'] = medhist_entries
    return render(request, 'ehr/view_ehr.html', http_dict)