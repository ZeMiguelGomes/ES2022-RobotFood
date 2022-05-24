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

@api_view(['GET'])
def getFoodItems(request):
    if request.method == 'GET':
        #sf = boto3.client('stepfunctions', region_name='us-east-1')
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id="ASIA5UAJKHAHMCM3DHHO", aws_secret_access_key="HJwINA/SrPTHTnFauAeeEwChPfnJRnLkXHt6J1uT", aws_session_token="FwoGZXIvYXdzEJf//////////wEaDEdymnZm/Yz9l2MXfiLLAegXb7svd0Z9NeTFT1ra6NPI0JlFmjOFGksAie4bTRjsHVdMOMw2bog3kzplOKvKZ/z3h57T6561wDGcibx/GSIDuc4qHbmfG+0BEzoJdw376tXjVHa4gxQPmHvAAobAr3a3QJEbu4+vs08x9AIPjZdk6eOGvirc317k/tCQu+csKtD/l20kjAXrco+m9bRua0MnC1aCLX3Z2n8xJITleGOrWCJxzJUFNSVmFKkAmc8lWeJmdGGxe9TMeevp4+aTNn6kRgkcj6lHxStlKIbPsZQGMi0sFPGSK4MAJsYoTySXZ9AOC4OwE/yPZNctRBKGsiXmBgGPsKIvoYJXXT83DMw=")
        
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
        s3 = boto3.client('s3', region_name='us-east-1', aws_access_key_id="ASIA5UAJKHAHMCM3DHHO", aws_secret_access_key="HJwINA/SrPTHTnFauAeeEwChPfnJRnLkXHt6J1uT", aws_session_token="FwoGZXIvYXdzEJf//////////wEaDEdymnZm/Yz9l2MXfiLLAegXb7svd0Z9NeTFT1ra6NPI0JlFmjOFGksAie4bTRjsHVdMOMw2bog3kzplOKvKZ/z3h57T6561wDGcibx/GSIDuc4qHbmfG+0BEzoJdw376tXjVHa4gxQPmHvAAobAr3a3QJEbu4+vs08x9AIPjZdk6eOGvirc317k/tCQu+csKtD/l20kjAXrco+m9bRua0MnC1aCLX3Z2n8xJITleGOrWCJxzJUFNSVmFKkAmc8lWeJmdGGxe9TMeevp4+aTNn6kRgkcj6lHxStlKIbPsZQGMi0sFPGSK4MAJsYoTySXZ9AOC4OwE/yPZNctRBKGsiXmBgGPsKIvoYJXXT83DMw=")
        s3.put_object(Body=data['file'], Bucket='face-to-detect', Key=data['file'].name)
        #object = s3.Object('face-to-detect', data['file'].name)
        #ret = object.put(Body=data['file'])

        return JsonResponse(True, safe=False)

@api_view(['POST'])  
def orderPrice(request):
    if request.method == 'POST':
        #sf = boto3.client('stepfunctions', region_name='us-east-1')
        sf = boto3.client('stepfunctions', region_name='us-east-1', aws_access_key_id="ASIA5UAJKHAHMCM3DHHO", aws_secret_access_key="HJwINA/SrPTHTnFauAeeEwChPfnJRnLkXHt6J1uT", aws_session_token="FwoGZXIvYXdzEJf//////////wEaDEdymnZm/Yz9l2MXfiLLAegXb7svd0Z9NeTFT1ra6NPI0JlFmjOFGksAie4bTRjsHVdMOMw2bog3kzplOKvKZ/z3h57T6561wDGcibx/GSIDuc4qHbmfG+0BEzoJdw376tXjVHa4gxQPmHvAAobAr3a3QJEbu4+vs08x9AIPjZdk6eOGvirc317k/tCQu+csKtD/l20kjAXrco+m9bRua0MnC1aCLX3Z2n8xJITleGOrWCJxzJUFNSVmFKkAmc8lWeJmdGGxe9TMeevp4+aTNn6kRgkcj6lHxStlKIbPsZQGMi0sFPGSK4MAJsYoTySXZ9AOC4OwE/yPZNctRBKGsiXmBgGPsKIvoYJXXT83DMw=")
        
        res = sf.start_sync_execution(stateMachineArn=calc_price, input=json.dumps(request.data['order']))
        data = json.loads(res["output"])
        print(data)

        return JsonResponse(data["total"], safe=False)
