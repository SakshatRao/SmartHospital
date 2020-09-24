from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied

from utils.access import patient_access, is_patient
from .models import Health_Status

import numpy as np
from datetime import datetime, timezone
import time

def http_dict_func(request):
    return {'is_patient': is_patient(request)}

@patient_access()
def homepage_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'patient/homepage.html', http_dict)

@patient_access()
def health_status_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'patient/patient_health_status.html', http_dict)

@patient_access()
def temperature_graph_view(request):
    health_status = Health_Status.objects.filter(patient_id = request.user.patient.id).order_by('recorded_time')
    time_diff = datetime.now(tz = None) - health_status[len(health_status) - 1].recorded_time.replace(tzinfo = None)
    if(time_diff.seconds > 10 * 60):
        return JsonResponse(data = {
            'temperatures': [0, 0, 0],
            'timeline': ['', '', ''],
            'axesLabelSize': 25,
            'axesLabel': 'Latest Data Not Available!',
            'axesLabelColor': 'red'
        })
    else:
        temperatures = [x.temperature for x in health_status]
        timeline = [x.recorded_time.strftime("%I:%M %p") for x in health_status]
        labelled_x = [0, len(timeline) // 3, 2 * len(timeline) // 3, len(timeline) - 1]
        timeline = [x if idx in labelled_x else '' for idx, x in enumerate(timeline)]
        return JsonResponse(data = {
            'temperatures': temperatures,
            'timeline': timeline,
            'axesLabelSize': 12,
            'axesLabel': '',
            'axesLabelColor': 'black'
        })