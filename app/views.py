from django.shortcuts import render, redirect
from .serializers import Userserializers, LoginSerializers,IncidentSerializers
from .models import *
from rest_framework import generics
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
import traceback
import json
import datetime

User = get_user_model()
# Create your views here.


def api_response(code,data,message,errors):
    res = {}
    res['code'] = code
    res['data'] = data
    res['message'] = message
    res['errors'] = errors
    return res

# def check_auth(request):
#     try:
#         header_data = request.headers["Authorization"]
#         user_id = 0
#         return True, user_id
#     except Exception as e:
#         print(e)

# Api starts from here 


class UserGetView(generics.GenericAPIView):
    def get(self, request):
        data = User.objects.all()
        instance = Userserializers(data,many=True)
        return Response(instance.data)


class UserRegisterView(generics.GenericAPIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        try:
            vaildation = Userserializers(data=request.data)
            if vaildation.is_valid():
                User.objects.create(username = vaildation.data['email_id'], email = vaildation.data['email_id'], password = make_password(vaildation.data['password']), phone_number = vaildation.data['phone_number'], state = vaildation.data['state'], country = vaildation.data['country'],fax = vaildation.data['fax'], pincode = vaildation.data['pincode'],address = vaildation.data['address'], city = vaildation.data['city'])
                return Response(vaildation.data)
            else:
                return Response(vaildation.error_messages)
        except Exception as e:
            print(e)
            return JsonResponse(api_response(1,[],"Error",str(e)))
        


class UserLoginView(generics.GenericAPIView):
    permission_classes = []
    def post(self,request):
        try:
            vaildation = LoginSerializers(data=request.data)
            if vaildation.is_valid():
                email = vaildation.data['email_id']
                password = vaildation.data['password']
                try:
                    user = User.objects.get(email = email)
                except User.DoesNotExist:
                    return Response("User does not exist") 
                
                if check_password(password,user.password):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({"message":"Login success fully ", "token":token.key})
                else:
                    return Response("Wrong Password")
        except Exception as e:
            print(e)
            return Response("Error occurred during login")



# def decode_token(token_key):
#     try:
#         token = Token.objects.get(key=token_key)
#         user = token.user
#         return user.id
#     except Token.DoesNotExist:
#         return None


def check_auth(request):
    try:
        header_data = request.headers["Authorization"]
        if 'Token' in header_data:
            encoded_token = header_data.split(' ')[1]
        else:
            raise ValueError("Token not present in Authorization header")
        token = Token.objects.get(key = encoded_token)
        user = token.user
        print(type(user.id))
        return True, user.id
    except Exception as e:
        print(e)
        return False, None






class CreateIncidentApi(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            auth_status, user_id = check_auth(request)
            validation = IncidentSerializers(data=request.data)
            if auth_status:
                if validation.is_valid():
                    user = get_object_or_404(User, id=user_id)
                    # print(user,"127")
                    Incident.objects.create(user=user,incident=validation.data['incident'],incident_modify_date=datetime.datetime.now())
                    return Response({"User ","incident created"})
            else:
                return Response("User Unautherized")
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({"message":"error"})
        


class GetAllIncident(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        try:
            auth_status, user_id = check_auth(request)
            if auth_status:
                instance = Incident.objects.all()
                validation = IncidentSerializers(instance,many=True)
                return Response(validation.data)
            else:
                return Response({'message':'The incident is not valid'})
        except Exception as e:
            print(e)
            return JsonResponse(api_response(1,[],"Error",str(e)))

  

class UpdateIncident(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self,request, id, *args, **kwargs):
        try:
            auth_status, user_id = check_auth(request)
            validation = IncidentSerializers(data=request.data)
            if auth_status:
                if validation.is_valid():
                    user = get_object_or_404(User, id=user_id)
                    Incident.objects.filter(id = id).update(user=user,incident=validation.data['incident'],incident_modify_date=datetime.datetime.now())
                    return Response({"updated","incident updated"})
            else:
                return Response("User Unautherized")
        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({"message":"error"})