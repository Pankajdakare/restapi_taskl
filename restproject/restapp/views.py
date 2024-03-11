# from django.shortcuts import render, HttpResponse

from django.views.decorators.csrf import csrf_exempt
# import io
from rest_framework.parsers import JSONParser
# from rest_framework.renderers import JSONRenderer
from restapp.serializers import ClientSerializer,ProjectSerialiser
# import json
from django.http import JsonResponse
from restapp.models import Client,Project
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
# from apiapp.serializers import UserSerialiser
from rest_framework.decorators import api_view
from rest_framework.serializers import ValidationError
from django.contrib.auth import authenticate, login, logout

@csrf_exempt
def Client(request):
    if request.method == "POST":
        # print('AUTH', request.user.is_authenticated)
        if request.user.is_authenticated:
            # s = request.body
            # print(s)
            # print(type(s)) #bytes
            # sdata = io.BytesIO(s) #byte to string
            # # print(sdata)
            # print(type(sdata)) #io.BytesIO
            # print(sdata)
            # dict1 = JSONParser().parse(sdata)
            # # print(dict1)
            # print(type(dict1)) #dict
            # serializer = StudentSerializer(data = dict1)

            data = JSONParser().parse(request)
            user = request.user
            data['uid'] = user.id
            data['addedBy'] = user.username
            # print('DATA TO BE ADDED', data)
            # print(type(data)) # dict
            # print(data)
            serializer = ClientSerializer(data = data) 
            # print(type(serializer)) 
            if serializer.is_valid():
                serializer.save() #stu.is_valid() must be called before this
                # resp = { 'response':'Student added !!!'}
                # json_resp = json.dumps(resp)
                # return HttpResponse(json_resp)
                data = serializer.data
                # data.remove('uid')
                return JsonResponse(data, status = status.HTTP_201_CREATED)
            else:
                # print('within else')
                return JsonResponse(serializer.errors,status= status.HTTP_400_BAD_REQUEST)
    else: #GET request
        data = Client.objects.all()
        #print(dict(students))
        ser = ClientSerializer(data,many=True)
        print(type(ser.data))
        # print(type(ser.data))
        return JsonResponse(ser.data,status=status.HTTP_200_OK,safe=False)
    
@csrf_exempt    
def clientDetails(request,sid):
    try:
        stu = Client.objects.get(id = sid)
    except ObjectDoesNotExist:
        error = {'error':'Invalid client id, client not found'}
        return JsonResponse(error,status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serialiser = ClientSerializer(stu)
        # print("ser data ------>\n",serialiser.data) # gives dict
        data = serialiser.data
        # data.remove('uid')
        return JsonResponse(data,status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        stu.delete()
        success = {'success':'cliient deleted !!'}
        return JsonResponse(success,status = status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        # print(data) here id is string
        data['id'] = sid
        data['id'] = int(data['id'])
        # print('updated',data)
        serializer = ClientSerializer(stu,data = data) 
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == "POST":        
        data = JSONParser().parse(request)
        # serializer = UserSerialiser(data = data)
        

        password = data['password']
        password2 = data['password2']
        if password != password2 :
            raise ValidationError({"Error":"password does not match"})
        
        if User.objects.filter(email = data['email']).exists():
            raise ValidationError({"Error":"email already exists"})
        
        account = User.objects.create_user(email = data['email'], username = data['username'], password = data['password'])
        account.save()
        
        return JsonResponse("Registered", status = status.HTTP_201_CREATED, safe = False) # In order to allow non-dict objects to be serialized set the safe parameter to False
    return ValidationError({'Error':'Invalid request'})

@api_view(['POST'])
def user_login(request):
    if request.method=="POST":
        data = JSONParser().parse(request)
        # print('DATA',data)
        u = data['username']
        p = data['password']
        
        user = authenticate(username = u, password = p)
        # print('LOGIN',user)
        if user is not None:
            # print(user)
            login(request,user)
            return JsonResponse({"success":"Logged in"},status = status.HTTP_200_OK)

def user_logout(request):
    # print(request.user.is_authenticated)
    if request.user.is_authenticated:
        user = request.user
        # print(user)
        logout(request)
        return JsonResponse({'success':"logged out"}, status = status.HTTP_200_OK)
    
@csrf_exempt
def Project(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(type(data))
        ser= ProjectSerialiser(data=data)
        if ser.is_valid():
            ser.save()
            return JsonResponse(ser.data,status=201)
        else:
            return JsonResponse(ser.errors ,status=400)
    else:
        data = Project.objects.all()
        ser = ProjectSerialiser(data, many= True)
        return JsonResponse(ser.data , status=200,safe=False)
