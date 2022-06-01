import boto3
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse

aws_access_key_id="ASIA5UAJKHAHF357WS6S"
aws_secret_access_key="9r1J/u9NasvauRJx6IYR1R8/eHX0QLudRTUZGtrR"
aws_session_token="FwoGZXIvYXdzEF8aDEtaBHkWpBpiBMSwfCLLAeWA+wUcaqPyFjAmCGb26yuoQiPvokG8dlcvDx3FM1NFeyLKlMt+K9c88DCFG1sdFmjYCynxE45PSISqfGI1GE0C+wvRG6n98YMCqTBRVvJAslCKMssqRGifY5HaSVfGBt63L7NnfPqnnnugEe4DG4Mq82DVtdtK+ZWHvXzsvD+XIQS2AYHW6m5lDoei99f/O1Ptx/IzwM3Mnldhlsx2MZ5LXqtHw92qd1mjdNkiOe4l3i0W1lvf/1bUG96zbj0urgSqdHqTbDepvLG6KOXP3ZQGMi1/rtncF+1bZW/H3zDreF6gmxRWz25gzXAfWv2om2Wl0wK8/zg70jVSBQHRzLY="

get_food_items = "arn:aws:states:us-east-1:936322414606:stateMachine:GetFoodItems"
calc_price = "arn:aws:states:us-east-1:936322414606:stateMachine:CalcPrice"
get_food_itemsZe = "arn:aws:states:us-east-1:067458896719:stateMachine:GetFoodItems"
calc_priceZe = "arn:aws:states:us-east-1:067458896719:stateMachine:calc_price"
submit_order = "arn:aws:states:us-east-1:936322414606:stateMachine:SubmitOrder"
facial_rekognition = "arn:aws:states:us-east-1:936322414606:stateMachine:FacialRekognition"

@api_view(['GET'])
def getFoodItems(request):
    if request.method == 'GET':
        #sf = boto3.client('stepfunctions', region_name='us-east-1')
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
        
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

@api_view(['GET', 'POST'])
def uploadPhoto(request):

    if request.method == 'GET':
        return render(request, 'customer/uploadphoto.html')

    if request.method == 'POST':
        data = request.data.dict()
        
        #s3 = boto3.client('s3', region_name='us-east-1')
        s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)

        s3.put_object(Body=data['file'], Bucket='face-to-detect', Key=data['file'].name)
        res = sf.start_sync_execution(stateMachineArn=facial_rekognition, input=json.dumps({"photoName": data['file'].name}))
        print(res["output"])
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
        res = sf.start_execution(stateMachineArn=submit_order, input=json.dumps(request.data))
        
        return JsonResponse("Order submitted!", safe=False)

@api_view(['POST'])  
def orderPrice(request):
    if request.method == 'POST':
        #sf = boto3.client('stepfunctions', region_name='us-east-1')
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
        
        res = sf.start_sync_execution(stateMachineArn=calc_price, input=json.dumps(request.data['order']))
        data = json.loads(res["output"])
        print(data)

        return JsonResponse(data["total"], safe=False)
