import boto3
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

@api_view(['GET'])
def getFoodItems(request):
    if request.method == 'GET':
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        return JsonResponse(dynamodb.Table('food_items').scan()['Items'], safe=False) #render(request, 'customer/menu.html')

@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        return render(request, 'customer/menu.html')