from rest_framework import serializers
from angApp.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class GeneratePairTokenSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username = username , password = password)
        
        if not user:
            raise AuthenticationFailed("No active User found with the given credentials !!") 
        
        if not user.check_password(password):
            raise AuthenticationFailed("Password does not match")
        
        #Generate Token
        refresh = RefreshToken.for_user(user)

        return {
            "status":200,
            "message":"User Login Successfully !!",
            "access_token": str(refresh.access_token),
            "refresh_token" :str(refresh) 
        }

