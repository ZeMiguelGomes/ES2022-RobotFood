
import boto3
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import JsonResponse
from botocore.exceptions import ClientError
from rest_framework.response import Response
from rest_framework import status
import jwt


KEY = "b96ZhIxcBdxNPDn4WRzDueMMqyux3k7g"
#Encrypt
#pwd_context = CryptContext(
#        schemes=["pbkdf2_sha256"],
#        default="pbkdf2_sha256",
#        pbkdf2_sha256__default_rounds=30000
#)


# Create your views here.

@api_view(['GET', 'POST'])
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

    if request.method == 'GET':
        return render(request, 'kitchen/insideLogin.html')

@api_view(['GET'])
def index(request):
    if request.method == 'GET':
        return render(request, 'kitchen/login.html')