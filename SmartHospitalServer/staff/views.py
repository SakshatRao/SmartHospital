from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from utils.access import http_dict_func, staff_access
from accounts.models import Patient, All_Patient
from patient.models import Health_Status
from django.contrib.auth.models import User

from datetime import datetime, date, timezone
import itertools
import time
import json

# Maximum time difference for health status of a patient to be plotted (in minutes)
MAX_TIME_DIFF = 10

# Homepage for Staff (requires staff login)
@staff_access()
def homepage_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'staff/homepage.html', http_dict)

# Page for staff to validate patients (requires staff login)
@staff_access()
def validate_patient(request):
    if(request.method == 'POST'):
        for key in request.POST:
            if(key != 'csrfmiddlewaretoken'):
                valid_user = User.objects.get(username = key)
                valid_user.patient.is_validated = True
                valid_all_patient = All_Patient.objects.get(patient_email = valid_user.email)
                valid_all_patient.patient = valid_user.patient
                valid_user.patient.save()
                valid_all_patient.save()
        return redirect('staff:homepage')
    else:
        patients = Patient.objects.all()
        unvalidated_patients = []
        for patient in patients:
            try:
                _ = patient.all_patient
            except:
                unvalidated_patients.append(patient)
        http_dict = http_dict_func(request)
        http_dict['unvalid_patients'] = unvalidated_patients
        return render(request, 'staff/validate_patient.html', http_dict)

# Page for staff to remove patients (requires staff login)
@staff_access()
def remove_patient(request):
    if(request.method == 'POST'):
        for key in request.POST:
            if(key != 'csrfmiddlewaretoken'):
                valid_user = User.objects.get(username = key)
                valid_all_patient = All_Patient.objects.get(patient_email = valid_user.email)
                valid_all_patient.discharge_date = date.today()
                valid_all_patient.save()
                valid_user.delete()
        return redirect('staff:homepage')
    else:
        patients = Patient.objects.all()
        validated_patients = []
        for patient in patients:
            try:
                _ = patient.all_patient
                validated_patients.append(patient)
            except:
                pass
        http_dict = http_dict_func(request)
        http_dict['valid_patients'] = validated_patients
        return render(request, 'staff/remove_patient.html', http_dict)

# Page for staff to view every patient's health status (requires staff login)
@staff_access()
def view_health_status(request):
    patients = Patient.objects.all()
    patients_health = []

    for patient in patients:
        health_status = patient.health_status_set.all()
        if(len(health_status) > 0):
            health_status = health_status.order_by('-recorded_time')[0]
            health_status_dict = {}
            health_status_dict['name'] = patient
            health_status_dict['patient_id'] = patient.id
            health_status_dict['room_number'] = patient.room_number
            health_status_dict['temperature'] = health_status.temperature
            health_status_dict['spO2'] = health_status.spO2
            health_status_dict['bpm'] = health_status.bpm
            health_status_dict['recorded_time'] = health_status.recorded_time.replace(tzinfo = None)
            patients_health.append(health_status_dict)
    
    http_dict = http_dict_func(request)
    http_dict['health_status'] = patients_health
    return render(request, 'staff/view_health_status.html', http_dict)

# Page for staff to view a particular patient's health status (requires staff login)
@staff_access()
def view_indiv_health_status(request):
    if(request.method == 'POST'):
        patient_id = [x for x in request.POST.keys() if x.startswith('ID_')]
        assert (len(patient_id) == 1)
        patient_id = int(patient_id[0].split('_')[1])
    http_dict = http_dict_func(request)
    http_dict['patient_id'] = patient_id
    return render(request, 'staff/indiv_health_status.html', http_dict)

# To view patient's temperature graph (requires staff login)
@staff_access()
def temperature_graph_view(request):
    if(request.method == 'GET'):
        patient_id = request.GET['patient_id']
        health_status = Health_Status.objects.filter(patient_id = patient_id).order_by('recorded_time')
        time_diff = datetime.now(tz = None) - health_status[len(health_status) - 1].recorded_time.replace(tzinfo = None)
        if(time_diff.seconds > MAX_TIME_DIFF * 60):
            return JsonResponse(data = {
                'temperatures': [0, 0, 0],
                'timeline': ['', '', ''],
                'axesLabelSize': 25,
                'axesLabel': 'Latest Data Not Available!',
                'axesLabelColor': 'red'
            })
        else:
            time_filter = [(datetime.now(tz = None) - x.recorded_time.replace(tzinfo = None)).seconds < MAX_TIME_DIFF * 60 for x in health_status]
            temperatures = list(itertools.compress([x.temperature for x in health_status], time_filter))
            timeline = list(itertools.compress([x.recorded_time.strftime("%I:%M %p") for x in health_status], time_filter))
            labelled_x = [0, len(timeline) - 1]
            timeline = [x if idx in labelled_x else '' for idx, x in enumerate(timeline)]
            return JsonResponse(data = {
                'temperatures': temperatures,
                'timeline': timeline,
                'axesLabelSize': 12,
                'axesLabel': '',
                'axesLabelColor': 'black'
            })

# To view patient's SpO2 graph (requires staff login)
@staff_access()
def spO2_graph_view(request):
    if(request.method == 'GET'):
        patient_id = request.GET['patient_id']
        health_status = Health_Status.objects.filter(patient_id = patient_id).order_by('recorded_time')
        time_diff = datetime.now(tz = None) - health_status[len(health_status) - 1].recorded_time.replace(tzinfo = None)
        if(time_diff.seconds > MAX_TIME_DIFF * 60):
            return JsonResponse(data = {
                'spO2s': [0, 0, 0],
                'timeline': ['', '', ''],
                'axesLabelSize': 25,
                'axesLabel': 'Latest Data Not Available!',
                'axesLabelColor': 'red'
            })
        else:
            time_filter = [(datetime.now(tz = None) - x.recorded_time.replace(tzinfo = None)).seconds < MAX_TIME_DIFF * 60 for x in health_status]
            spO2s = list(itertools.compress([x.spO2 for x in health_status], time_filter))
            timeline = list(itertools.compress([x.recorded_time.strftime("%I:%M %p") for x in health_status], time_filter))
            labelled_x = [0, len(timeline) - 1]
            timeline = [x if idx in labelled_x else '' for idx, x in enumerate(timeline)]
            return JsonResponse(data = {
                'spO2s': spO2s,
                'timeline': timeline,
                'axesLabelSize': 12,
                'axesLabel': '',
                'axesLabelColor': 'black'
            })

# To view patient's BPM graph (requires staff login)
@staff_access()
def bpm_graph_view(request):
    if(request.method == 'GET'):
        patient_id = request.GET['patient_id']
        health_status = Health_Status.objects.filter(patient_id = patient_id).order_by('recorded_time')
        time_diff = datetime.now(tz = None) - health_status[len(health_status) - 1].recorded_time.replace(tzinfo = None)
        if(time_diff.seconds > MAX_TIME_DIFF * 60):
            return JsonResponse(data = {
                'bpms': [0, 0, 0],
                'timeline': ['', '', ''],
                'axesLabelSize': 25,
                'axesLabel': 'Latest Data Not Available!',
                'axesLabelColor': 'red'
            })
        else:
            time_filter = [(datetime.now(tz = None) - x.recorded_time.replace(tzinfo = None)).seconds < MAX_TIME_DIFF * 60 for x in health_status]
            bpms = list(itertools.compress([x.bpm for x in health_status], time_filter))
            timeline = list(itertools.compress([x.recorded_time.strftime("%I:%M %p") for x in health_status], time_filter))
            labelled_x = [0, len(timeline) - 1]
            timeline = [x if idx in labelled_x else '' for idx, x in enumerate(timeline)]
            return JsonResponse(data = {
                'bpms': bpms,
                'timeline': timeline,
                'axesLabelSize': 12,
                'axesLabel': '',
                'axesLabelColor': 'black'
            })