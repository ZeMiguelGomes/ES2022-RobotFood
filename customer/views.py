import boto3
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse

aws_access_key_id="ASIA5UAJKHAHFEDTXGYV"
aws_secret_access_key="PyXZ0QEuyewlIAXq/uDCtUqI5ptEFSW47TDhUAtk"
aws_session_token="FwoGZXIvYXdzEGYaDKLQPKNd5F0Vfe3+CCLLAXe6bqNzu7la/EyXTZBy1ig7VOx9BsAV55o+Z+DU/QH5eSEkpQiNvqGkd3+ZAl9Wzz3de+nmDx3wEDN2rqXo603G77Zscm6Fm50Y02p7QPoIgcnULUh1gzwcsOCfZQU+AuJSvoBCVBJtYfKMi/V8JvfTEX7Zx/fFerTsZz4nMNtairIoiRhTPiYQYqHWT18vQLbi5FsmGPdOtNEbRz1T78Z78eO7emJOhX5zp0DmZ3WvJnogzWSHMo3diEbAypj11T6DGp/irF4Y14CbKLij35QGMi1gDfxW/YHu3Yqh+LeWVV2cTx/htAcBC375cFf2j7krbRP/nONv0sqMS+XcWu8="
get_food_items = "arn:aws:states:us-east-1:936322414606:stateMachine:GetFoodItems"
calc_price = "arn:aws:states:us-east-1:936322414606:stateMachine:CalcPrice"

get_food_itemsZe = "arn:aws:states:us-east-1:067458896719:stateMachine:GetFoodItems"
calc_priceZe = "arn:aws:states:us-east-1:067458896719:stateMachine:calc_price"
submit_orderZe = "arn:aws:states:us-east-1:067458896719:stateMachine:submit_order"
facial_rekognitionZe = "arn:aws:states:us-east-1:067458896719:stateMachine:FacialRekognition"

retrieve_order = "arn:aws:states:us-east-1:936322414606:stateMachine:RetrieveOrder"
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
        
        res = sf.start_sync_execution(stateMachineArn=submit_order, input=json.dumps(request.data))
        
        return JsonResponse(res["output"], safe=False)

@api_view(['POST'])  
def orderPrice(request):
    if request.method == 'POST':
        #sf = boto3.client('stepfunctions', region_name='us-east-1')
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
        
        res = sf.start_sync_execution(stateMachineArn=calc_price, input=json.dumps(request.data['order']))
        data = json.loads(res["output"])
        print(data)

        return JsonResponse(data["total"], safe=False)

@api_view(['PUT'])
def retrieveOrder(request):
    if request.method == 'PUT':
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key , aws_session_token=aws_session_token)
        res = sf.start_sync_execution(stateMachineArn=retrieve_order, input=json.dumps(request.data))
        res = json.loads(res["output"])
        print(res["Item"]["progress"]["S"])
        return JsonResponse("retrieve", safe=False)

