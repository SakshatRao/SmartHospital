from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied

from utils.access import patient_access, http_dict_func
from .models import Health_Status

import numpy as np
from datetime import datetime, timezone
import time
import itertools

# Maximum time difference allowed for showing health status graphs (in minutes)
MAX_TIME_DIFF = 10

# Homepage for patients (requires patient login)
@patient_access()
def homepage_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'patient/homepage.html', http_dict)

# For viewing health status graphs (requires patient login)
@patient_access()
def health_status_view(request):
    http_dict = http_dict_func(request)
    http_dict['patient_id'] = request.user.patient.id
    return render(request, 'patient/patient_health_status.html', http_dict)

# For accessing temperature values (requires patient login)
@patient_access()
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

# For accessing SpO2 values (requires patient login)
@patient_access()
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

# For accessing BPM values (requires patient login)
@patient_access()
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