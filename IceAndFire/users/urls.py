from django.urls import path
from rest_framework.authtoken import views

from .api import CreateUser


app_name = 'users'

urlpatterns = [
    # /users/register
    path('register', CreateUser.as_view(), name='register'),
    # /users/login
    path('login', views.obtain_auth_token, name='login'),
]
