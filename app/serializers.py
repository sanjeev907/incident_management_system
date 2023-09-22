from rest_framework import serializers
from .models import *

class Userserializers(serializers.Serializer):

    email_id = serializers.CharField(required = True, error_messages = {"email_id":'email_id is required'})
    password = serializers.CharField(required = True, error_messages = {"password":'password is required'})
    phone_number = serializers.CharField(required = True, error_messages = {"phone_number":'phone_number is required'})
    state = serializers.CharField(required = True, error_messages = {"state":'state is required'})
    country = serializers.CharField(required = True, error_messages = {"country":'country is required'})
    fax = serializers.CharField(required = True, error_messages = {"fax":'fax is required'})
    pincode = serializers.CharField(required = True, error_messages = {"pincode":'pincode is required'})
    address = serializers.CharField(required = True, error_messages = {"address":'address is required'})
    city = serializers.CharField(required = True, error_messages = {"city":'city is required'})
    

class LoginSerializers(serializers.Serializer):
    email_id = serializers.CharField(required = True, error_messages = {"email_id":'email_id is required'})
    password = serializers.CharField(required = True, error_messages = {"password":'password is required'})


class IncidentSerializers(serializers.Serializer):
    incident = serializers.CharField()