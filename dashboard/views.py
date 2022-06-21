from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def dashboard_map(request):
    return HttpResponse("It works!")