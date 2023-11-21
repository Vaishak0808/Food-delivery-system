from django.urls import path,include
from login.views import UserLoginAPI

urlpatterns = [
    path('userlogin/',UserLoginAPI.as_view()),
    
]