import boto3
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse

get_food_items = "arn:aws:states:us-east-1:936322414606:stateMachine:GetFoodItems"

@api_view(['GET'])
def getFoodItems(request):
    if request.method == 'GET':
        sf = boto3.client('stepfunctions', region_name='us-east-1')
        res = sf.start_sync_execution(stateMachineArn=get_food_items)
        data = json.loads(res["output"])
        
        return JsonResponse(data, safe=False)

@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        return render(request, 'customer/menu.html')

@api_view(['GET'])
def mainMenu(request):
    if request.method == 'GET':
        return render(request, 'customer/mainMenu.html')