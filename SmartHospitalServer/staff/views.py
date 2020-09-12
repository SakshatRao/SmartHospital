from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from utils.access import http_dict_func, staff_access

@staff_access()
def homepage_view(request):
    http_dict = http_dict_func(request)
    return render(request, 'staff/homepage.html', http_dict)