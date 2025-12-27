from rest_framework import serializers
from angApp.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
import re
User = get_user_model()



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','category_name','slug_url','meta_title','meta_description','created')



class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()

    def create(self , validated_data):
        category_name = validated_data.get('category_name')
        slug_url = self.normalize(category_name)
        validated_data['slug_url'] = slug_url
        validated_data['slug'] = category_name
        # category = Category.objects.create(**validated_data)
        # return category
        return super().create(validated_data)


    def normalize(self, text):
        text = text.lower()
        text = text.replace('&', 'and')
        text = re.sub(r'\s+', '-', text)      
        text = re.sub(r'[^a-z0-9-]', '', text)  
        return text


    def get_sub_category(self, obj):
        sub_category = Category.objects.filter(parent = obj.id)
        return SubCategorySerializer(sub_category , many=True).data


    class Meta:
        model = Category
        fields= ('id','category_name','slug_url','meta_title','meta_description','sub_category','created')





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


class UserInfoDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfoDetails
        exclude = ('user',)



class UserCreateSerializer(serializers.ModelSerializer):
    user_info = UserInfoDetailsSerializer()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields  = ('username','email','password','user_info','confirm_password')


    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise APIException( "Password and confirm password do not match.")

        if len(password) < 8:
            raise APIException( "Password must be at least 8 characters long.")

        return attrs


    def create(self, validated_data):
        user_info_data = validated_data.pop('user_info')
        confirm_password = validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        UserInfoDetails.objects.create(
            user = user,
            **user_info_data
        )
        return user