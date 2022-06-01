import boto3
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse

aws_access_key_id="ASIAQ7NG5CNH54SBJAHA"
aws_secret_access_key="7jHL34r+xMjj7wAukw3OZmHbd7Po8aqqOpeMsPW8"
aws_session_token="FwoGZXIvYXdzEGAaDPv6eMd2KlqJPL8QEiLLAavr2KFHmpgJJfRP84MsD69KMDrCrYtg83LrotuuPtVgYe7ZbrSrVmG6v+7pB7KDNuCIA9NWJ9qj2U4jRj61cTaPOtVkQVpm9RxksAq9q6wSo6QvgyRbCS5Vc+AaAAexT/lgk/AXhULjugZK/cJNFh/YMLfP6A5rY+yt2YKFILgkMOY4uLSdQb9Abo1uHfscm00/gjNlUlDcpucpoqAqvME+h9inRgABD1NXeZMsZaBC5vKybFrLoR4aMaG5pjjKIPSY/0o0kWDFJVeVKMT+3ZQGMi3ObZ8SniCmn0nXToJQ6Cbyd7U5UCEMmeLlk+uo1kOS52SeeFGCvkeeQou/Mak="

get_food_items = "arn:aws:states:us-east-1:936322414606:stateMachine:GetFoodItems"
calc_price = "arn:aws:states:us-east-1:936322414606:stateMachine:CalcPrice"

get_food_itemsZe = "arn:aws:states:us-east-1:067458896719:stateMachine:GetFoodItems"
calc_priceZe = "arn:aws:states:us-east-1:067458896719:stateMachine:calc_price"
submit_orderZe = "arn:aws:states:us-east-1:067458896719:stateMachine:submit_order"
facial_rekognitionZe = "arn:aws:states:us-east-1:067458896719:stateMachine:FacialRekognition"


submit_order = "arn:aws:states:us-east-1:936322414606:stateMachine:SubmitOrder"
facial_rekognition = "arn:aws:states:us-east-1:936322414606:stateMachine:FacialRekognition"

@api_view(['GET'])
def getFoodItems(request):
    if request.method == 'GET':
        #sf = boto3.client('stepfunctions', region_name='us-east-1')
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
        
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
        s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)

        s3.put_object(Body=data['file'], Bucket='facetodetect-es', Key=data['file'].name)
        res = sf.start_sync_execution(stateMachineArn=facial_rekognitionZe, input=json.dumps({"photoName": data['file'].name}))
        print(res)
        return JsonResponse(res["output"], safe=False)

@api_view(['GET', 'POST'])
def submitOrder(request):

    if request.method == 'GET':
        return render(request, 'customer/uploadphoto.html')

    if request.method == 'POST':
        print(request.data)
        #sf = boto3.client('stepfunctions', region_name='us-east-1')
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)

        items = []
        for i in request.data["items"]:
            items.append(i["name"])

        request.data["items"] = items
        request.data["price"] = str(request.data["price"])
        print(type(request.data['price']))
        print(request.data)
        res = sf.start_execution(stateMachineArn=submit_orderZe, input=json.dumps(request.data))
        
        return JsonResponse("Order submitted!", safe=False)

@api_view(['POST'])  
def orderPrice(request):
    if request.method == 'POST':
        #sf = boto3.client('stepfunctions', region_name='us-east-1')
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
        
        res = sf.start_sync_execution(stateMachineArn=calc_priceZe, input=json.dumps(request.data['order']))
        data = json.loads(res["output"])
        print(data)

        return JsonResponse(data["total"], safe=False)
