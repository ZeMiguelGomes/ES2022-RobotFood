import boto3
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse

aws_access_key_id="ASIAQ7NG5CNH7G46PWNL"
aws_secret_access_key="gDbjUte8Jxih4oM5JVBoIfZqtNk5RIkN0sEe65OJ"
aws_session_token="FwoGZXIvYXdzEGUaDFArkJuC8aF7SbCVSSLLAT82EjYFrmZKHpyGvGP9/55UX1DxRECKGjqaaXDvgj+Sc8lGrpSuXwpOEeKfw9x8//Q/TbHyhxb9KQhIyKkJ2t4SA8OCkFNsKhOHKhyGx89mf6dBmL2iKcfrOelXCpQzHr+br6XPET5cWB6ZZ1lhg9YY6kwKBWlLomakVooExbyg0BVoDw/bd9v+pInHbrNvAiko8Mi/oyMGrdACPN6DxghXNm35mVF3DSjZmlTkfoj3AWNrL7EJHyVH3yqQVqbbjQ7Nk+0gI85blqj+KKTx3pQGMi0Tv3B6dIoe5OARBdeuqqYLgj48wZsLlSbnmX5ot3ZYMEnJm3qowm8/LMgUQKs="


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
