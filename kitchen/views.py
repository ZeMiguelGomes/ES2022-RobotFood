import boto3
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

@api_view(['GET','POST'])
def index(request):
    if request.method == 'POST':
        # Logica de Verificacao de Log In
        print(request.data)
        return JsonResponse({"logged": True})

    if request.method == 'GET':
        return render(request, 'kitchen/login.html')