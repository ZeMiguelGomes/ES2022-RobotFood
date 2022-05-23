import json
import re
import boto3
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import JsonResponse
from botocore.exceptions import ClientError
from rest_framework.response import Response
from rest_framework import status
import jwt


import psycopg2
import sys
import os

from .models import Staff
from .serializers import *

@api_view(['GET'])
def dbTest(request):
    if request.method == 'GET':
        data = Staff.objects.all()
        resposta = {"OBJ" : data}

        #serializer = StaffSerializer(data)
        return JsonResponse(resposta, safe=False)

   


KEY = "b96ZhIxcBdxNPDn4WRzDueMMqyux3k7g"
#Encrypt
#pwd_context = CryptContext(
#        schemes=["pbkdf2_sha256"],
#        default="pbkdf2_sha256",
#        pbkdf2_sha256__default_rounds=30000
#)

# Create your views here.

@api_view(['GET', 'POST', 'PUT'])
def loginStaff(request):
   
    if request.method == 'POST':
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        try:
            response = dynamodb.Table('kitchen_staff').get_item(
                Key={'staff_email': request.data['username']}
            )
        except ClientError as e:
            print(e.response['Error']['Message'])

        # Logica de Verificacao de Log In
        else:
            #Check if the response has something
            if 'Item' in response:
                #The emails exists
                if response['Item']['password'] == request.data['password']:
                    #We need to authenticate
                    token = jwt.encode(response['Item'], KEY)
                    #Colocar o TOKEN na BD e update ao boolean
                    update = dynamodb.Table('kitchen_staff').update_item(                                       
                        Key={'staff_email': request.data['username']},
                        UpdateExpression="set authToken = :r, isLoggedIn = :s",
                        ExpressionAttributeValues={
                            ':r': token,
                            ':s': 'True'
                        },
                        ReturnValues="ALL_NEW"
                    )
                    print("Sucess")
                    return JsonResponse(update, safe=False)
                else:
                    #Wrong password
                    return JsonResponse(None, safe=False)
            else:
                return JsonResponse(None, safe=False)

    """ if request.method == 'GET':
        if(len(request.data) == 0):
            return render(request, 'kitchen/login.html')
        return render(request, 'kitchen/insideLogin.html') """

    if request.method == 'GET':
        return render(request, 'kitchen/insideLogin.html')

    if request.method == 'PUT':
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

            try:
                response = dynamodb.Table('kitchen_staff').get_item(
                    Key={'staff_email': request.data['username']}
                )
            except ClientError as e:
                print(e.response['Error']['Message'])

            else:
                
                update = dynamodb.Table('kitchen_staff').update_item(                                       
                        Key={'staff_email': request.data['username']},
                        UpdateExpression="set authToken = :r, isLoggedIn = :s",
                        ExpressionAttributeValues={
                            ':r': '',
                            ':s': 'False'
                        },
                        ReturnValues="ALL_NEW"
                    )
            return render(request, 'kitchen/login.html')






get_ordersZe = 'arn:aws:states:us-east-1:067458896719:stateMachine:GetOrders'
@api_view(['GET'])
def getOrders(request):
    if request.method == 'GET':
        sf = boto3.client('stepfunctions', region_name='us-east-1')
        res = sf.start_sync_execution(stateMachineArn=get_ordersZe)
        data = json.loads(res["output"])
        return JsonResponse(data, safe=False)



@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        return render(request, 'kitchen/login.html')