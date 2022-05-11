from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import json
import os

def index(request):
    return HttpResponse("QQR COISA")