from django.shortcuts import render
from urllib import request,response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny,BasePermission
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import AccessToken



class IsTokenValid(BasePermission):
    def has_permission(self,request,view):
        token = request.headers.get('Authorization' ,None)
        if not token:
            raise APIException('Token is invalid or Expired.')
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
                access_token = AccessToken(token)
            else:
                raise APIException("Token cannot be empty")
        except Exception as e:
            raise APIException(e)
        return True



@api_view(['POST'])
@permission_classes([AllowAny])
def loginUser(request):
    serializerToken = GeneratePairTokenSerializer(data = request.data)
    if serializerToken.is_valid():
        return Response(serializerToken.validated_data , status=status.HTTP_200_OK)
    return Response(serializerToken.errors , status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsTokenValid])
def dashboard(request):
    return Response({"status":200 , 'data':"Dashboard api is working !!"} , status=status.HTTP_200_OK)