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


@api_view(['POST'])
@permission_classes([IsTokenValid])
def addCategory(request):
    if request.method == 'POST':
        serializers = CategorySerializer(data = request.data)
        if serializers.is_valid(raise_exception= True):
            category = serializers.save()
            return Response({'status':201,'message':'Category Created Successfully !','data':category.id} , status=status.HTTP_201_CREATED)
        return Response({'status':400 , 'message':'Failed to Create Category !'} , status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET" , "POST"])
@permission_classes([IsTokenValid])
def categoryList(request):
    try:
        category_id = request.data.get('id')
        if category_id:
            categoryData = Category.objects.filter(id= request.data).filter(deleted = False)
        else:
            categoryData = Category.objects.filter(parent = 0).filter(deleted = False)
        if categoryData:
            serializersData = CategorySerializer(categoryData , many = True)
            return Response({'status': 200 , 'data':  serializersData.data} , status = status.HTTP_200_OK)
        return Response({'status':400 , 'message':'No Category Found'} , status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
            raise APIException(e)

@api_view(['POST'])
@permission_classes([IsTokenValid])
def addUser(request):
    if request.method == 'POST':
        serializers = UserCreateSerializer(data = request.data)
        if serializers.is_valid(raise_exception = True):
            user = serializers.save()
            return Response({'status':201,'message':'User Created Successfully !','user':user.id} , status=status.HTTP_201_CREATED)
        return Response({'status':400 , 'message':'Failed to Create User !'} , status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsTokenValid])
def getUsersList(request):
    if request.method == 'GET':
        try:
            user = User.objects.all()
            if user:
                userSerializer = UserCreateSerializer(user , many = True)
                return Response({'status':200,'data':userSerializer.data } , status=status.HTTP_200_OK)
            return Response({'status':404, 'message':'No Data Found'} , status=status.HTTP_404_NOT_FOUND)
        except IsTokenValid as e:
            return Response({'status': e.status_code, 'message': str(e)}, status=e.status_code)