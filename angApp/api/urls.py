from django.urls import path,re_path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login-user',loginUser,name="loginUser"),
    path('token/refresh' ,TokenRefreshView.as_view() ,name='token_refresh'),
    path('dashboard',dashboard,name="dashboard"),
    path('add-user',addUser,name="add_user"),
    path('user-list',getUsersList,name="user_list"),
    path('add-category',addCategory , name="add_category"),
    path('category-list',categoryList , name="category_list")
]