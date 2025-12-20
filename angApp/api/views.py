from django.shortcuts import render
from urllib import request,response
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def loginUser(request):
    return Response({'status':201,'message':'User Created Successfully !'})