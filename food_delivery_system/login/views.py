from django.shortcuts import render
from django.contrib.auth import authenticate, login ,logout
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_201_CREATED,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR


# Create your views here.



class UserLoginAPI(APIView):
    permissions_classes = [AllowAny]
    def post(self,request):
        try:
            if request.data.get('PassWord') and request.data.get('username'):
                str_username = request.data.get('username')
                str_password = request.data.get('PassWord')
                user = authenticate(request, username=str_username, password=str_password)
                if user:
                    login(request, user)
                    return Response({"Message":"Login Successfully"},status=HTTP_200_OK)
                return Response({'Message':"Invalid Username or Password"},status = HTTP_400_BAD_REQUEST)
            return Response({'Message':"Username and Password are madatory"},status = HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Message':str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request):
        try:
            if request.user:
                logout(request)
                return Response({"Message":"Logout successfully"},status = HTTP_200_OK)
            return Response({'Message':"Something went wrong"},status = HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Message':str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)

class UserAPI(APIView):
    def get(aelf,request):
        try:
            pass
        except Exception as e:
            return Response({"Message":str(e)},status=HTTP_500_INTERNAL_SERVER_ERROR)