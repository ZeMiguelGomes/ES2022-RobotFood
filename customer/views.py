import boto3
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse

aws_access_key_id="ASIAQ7NG5CNH6GBRPVNK"
aws_secret_access_key="hsikC+Gfg2VRUPkWlfY2Bj+dpr2I9gEXTXEdzJnV"
aws_session_token="FwoGZXIvYXdzEGcaDOory8SBx6pkSu34/SLLAVmPMwmZ31fHJnqVgrQJacUZw8To3p71+iWNnBerobwKbZ1w/bOxvckR42df2IYHZC9bJEeq9OnDZgROtDatRNpMVOCAgI4jUvtKv8nrW6WwnyJL3RolJlQkiDu853KLi/rs0aKHzt/17FsK0Tce1rd2+x1TcooONJKAhvEZX5M/y5SgBGdqYbPmw8k5QLCBxI+IBCeplCn2D7NT0xSQ0f2oIb6z4nSMqp5kCsa3rTOgxX6YfBySqjwAVbTa2GsxRMRHbLw/HeQsM2IbKN2t35QGMi1w5PwlRL8wzghiOuFOo9zMj8PR4UPYMjPPWZX6g4JFPZmVZrftsK5dMfgFTnU="

get_food_items = "arn:aws:states:us-east-1:936322414606:stateMachine:GetFoodItems"
calc_price = "arn:aws:states:us-east-1:936322414606:stateMachine:CalcPrice"

get_food_itemsZe = "arn:aws:states:us-east-1:067458896719:stateMachine:GetFoodItems"
calc_priceZe = "arn:aws:states:us-east-1:067458896719:stateMachine:calc_price"
submit_orderZe = "arn:aws:states:us-east-1:067458896719:stateMachine:submit_order"
facial_rekognitionZe = "arn:aws:states:us-east-1:067458896719:stateMachine:FacialRekognition"
retrieve_orderZe = 'arn:aws:states:us-east-1:067458896719:stateMachine:retrieve_order'
DeliveredMealZe = 'arn:aws:states:us-east-1:067458896719:stateMachine:DeliveredMeal'


retrieve_order = "arn:aws:states:us-east-1:936322414606:stateMachine:RetrieveOrder"
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
        
        res = sf.start_sync_execution(stateMachineArn=submit_orderZe, input=json.dumps(request.data))
        
        return JsonResponse(res["output"], safe=False)

@api_view(['POST'])  
def orderPrice(request):
    if request.method == 'POST':
        #sf = boto3.client('stepfunctions', region_name='us-east-1')
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
        
        res = sf.start_sync_execution(stateMachineArn=calc_priceZe, input=json.dumps(request.data['order']))
        data = json.loads(res["output"])
        print(data)

        return JsonResponse(data["total"], safe=False)

@api_view(['PUT'])
def retrieveOrder(request):
    if request.method == 'PUT':
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
        res = sf.start_sync_execution(stateMachineArn=retrieve_orderZe, input=json.dumps(request.data))
        res = json.loads(res["output"])

        if(res["Item"]["progress"]["S"] == 'Ready' and res["Item"]['locationTag']['N'] == request.data['locationTag']):
            sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
            res = sf.start_sync_execution(stateMachineArn=DeliveredMealZe, input=json.dumps(res["Item"]['order_id']))
            return JsonResponse("Sucess", safe=False)
        print(res["Item"]["progress"]["S"])
        return JsonResponse("Error", safe=False)

