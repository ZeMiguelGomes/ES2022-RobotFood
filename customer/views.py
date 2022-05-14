import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.

@api_view(['GET','POST'])
def index(request):
    if request.method == 'POST':
        print(request.data)
        return Response(json.dumps(request.data))

    if request.method == 'GET':
        return render(request, 'kitchen/login.html')