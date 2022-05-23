import boto3
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse

get_food_items = "arn:aws:states:us-east-1:936322414606:stateMachine:GetFoodItems"
get_food_itemsZe = "arn:aws:states:us-east-1:067458896719:stateMachine:GetFoodItems"

@api_view(['GET'])
def getFoodItems(request):
    if request.method == 'GET':
        sf = boto3.client('stepfunctions', region_name='us-east-1')
        res = sf.start_sync_execution(stateMachineArn=get_food_itemsZe)
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
@api_view(['GET', 'POST'])
def uploadPhoto(request):

    if request.method == 'GET':
        return render(request, 'customer/uploadphoto.html')

    if request.method == 'POST':
        data = request.data.dict()
        
        #s3 = boto3.client('s3', region_name='us-east-1')
        s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id="ASIA5UAJKHAHOP6CCDWM", aws_secret_access_key="4PR8R/zZJcjwNjge7K0amiIpYum+/c7DPzmDXuZa", aws_session_token="FwoGZXIvYXdzEFgaDP/K+5dnCla0JwkbzSLLAeHjQkZ8wZwZG9bijBB2ywqv4OB1FO/y5N+BJ8TkVYbTsdiFKALrktDOl7f7d++dTgeDflUJ2OdCNKXjHwZ3DHQuP6vfvFaRtnuDzLQ3WGrNZE03O+f+RS8w0qzOYHQIoyofPa+8UMvW8T09+5qcjay9uNUC7RdV0o1TcFZomFEPwmxlMSc/6E5CH+1mhVN7FAoISQXAApiR/pqfz6sv1j2L3+b3ptbEPQhx3syV03j/xnTWrDpPZg5mP/xY0S56NXtITtq8/L9xDHOfKOb1o5QGMi0Qxq432sGFFIMJOIpM8HK7/kpeT3iXK1aVudEi/BZXGWzoT7+F/8ox3l4CCZU=")

        s3.put_object(Body=data['file'], Bucket='face-to-detect', Key=data['file'].name)
        #object = s3.Object('face-to-detect', data['file'].name)
        #ret = object.put(Body=data['file'])
        return JsonResponse(True, safe=False)

@api_view(['POST'])  
def orderPrice(request):
    if request.method == 'POST':
        price = 0
        return JsonResponse(price, safe=False)
