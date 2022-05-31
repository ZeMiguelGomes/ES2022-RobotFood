import boto3
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse

get_food_items = "arn:aws:states:us-east-1:936322414606:stateMachine:GetFoodItems"
calc_price = "arn:aws:states:us-east-1:936322414606:stateMachine:CalcPrice"
get_food_itemsZe = "arn:aws:states:us-east-1:067458896719:stateMachine:GetFoodItems"
calc_priceZe = "arn:aws:states:us-east-1:067458896719:stateMachine:calc_price"

@api_view(['GET'])
def getFoodItems(request):
    if request.method == 'GET':
        sf = boto3.client('stepfunctions', region_name='us-east-1')
        #sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id="ASIAQ7NG5CNH73SBWST6", aws_secret_access_key="aoRQCnDTIJZGwYeUO0BGthp2859KZ6ZX7zh4n5OU", aws_session_token="FwoGZXIvYXdzEJr//////////wEaDEuh2WBu4jdO5m9WQSLLAfXsgJHyQaAjY3fJmLDeWtlWfu9e6Mzi4RoXSPn6XfyB/QcLlqFl2J1yDSZE1SrwSy3R/6UHQ/4U1huGoSNN3ec364+bB5ujcILkJk/HsZTrwLZNSp9f5n3Y5P7HowHiQkgKgzF65jfzy4cBU0T5y2sjsVGjHJ1+nTafyMk0RfUxJjfy5GEXDrsFmXeBn0mdsJfukO94dBxeCcH2XQuSeQIKdO0JVy80q89JR+DQ7m6wcDbjcAq/GEwQ1QVTfLqafb8NPNQqubmFhie1KLu3spQGMi3imZFy63Ie+A6JvVydiQ6XxylJnb7YTxb1N9K/cHjQIinx+U5XQCEFe4WA8UU=")
        
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
        print(data)
        s3 = boto3.client('s3', region_name='us-east-1')
        #s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id="ASIAQ7NG5CNHSVKAVRNZ", aws_secret_access_key="k1YoeJjhoN4xkQLe5A6ngXowkL+pFMDD2jMuMkrM", aws_session_token="FwoGZXIvYXdzEKP//////////wEaDO6wrjs8Gu4R+xKVQSLLAVvgUyQkzcIm6WSHZ16AjNJXKTbtTxdQfaH8oa+56Vz4TwDAjTaCoQDl7TZDpz/Pd3XAjDVpvllf39De8fXJLo77mp1RMwjgfO0siXcMHTKshQ+sA+/8IVE73nML5+RGUMysTSkXdHWSLaEOobVPBEWuMz3I9jXGndmTH+BDqxNVfte4sJx9brj6WWDYwvRMbbyu3GuPnku1oRZ9MLs6fBwcoZakO/goWCeEOncMDsLQHGCyuG3kmVN4UNJBEmZd+N8/sU5PgwUoSAKGKLuttJQGMi384c8WHp6EVkQp2lIqnaehENv9KRrC949D1oqHgQlj0b63R9IO57POtWskTnY=")
        s3.put_object(Body=data['file'], Bucket='face-to-detect', Key=data['file'].name)
        #object = s3.Object('face-to-detect', data['file'].name)
        #ret = object.put(Body=data['file'])

        
        return JsonResponse(True, safe=False)

@api_view(['POST'])  
def orderPrice(request):
    if request.method == 'POST':
        sf = boto3.client('stepfunctions', region_name='us-east-1')
        #sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id="ASIAQ7NG5CNH73SBWST6", aws_secret_access_key="aoRQCnDTIJZGwYeUO0BGthp2859KZ6ZX7zh4n5OU", aws_session_token="FwoGZXIvYXdzEJr//////////wEaDEuh2WBu4jdO5m9WQSLLAfXsgJHyQaAjY3fJmLDeWtlWfu9e6Mzi4RoXSPn6XfyB/QcLlqFl2J1yDSZE1SrwSy3R/6UHQ/4U1huGoSNN3ec364+bB5ujcILkJk/HsZTrwLZNSp9f5n3Y5P7HowHiQkgKgzF65jfzy4cBU0T5y2sjsVGjHJ1+nTafyMk0RfUxJjfy5GEXDrsFmXeBn0mdsJfukO94dBxeCcH2XQuSeQIKdO0JVy80q89JR+DQ7m6wcDbjcAq/GEwQ1QVTfLqafb8NPNQqubmFhie1KLu3spQGMi3imZFy63Ie+A6JvVydiQ6XxylJnb7YTxb1N9K/cHjQIinx+U5XQCEFe4WA8UU=")
        
        res = sf.start_sync_execution(stateMachineArn=calc_price, input=json.dumps(request.data['order']))
        data = json.loads(res["output"])
        print(data)

        return JsonResponse(data["total"], safe=False)
