
from django.contrib import admin
from django.urls import path,include
from .views import login_view,register_view,logout_view

app_name="app_user_profile"

urlpatterns = [
    path('login',login_view,name="login_view"),
    path('logout',logout_view,name="logout_view"),
    path('register',register_view,name="register_view"),
]
