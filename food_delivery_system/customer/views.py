from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_201_CREATED,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
import re
from django.contrib.auth.models import User
import random
from django.db import transaction
from login.models import UserDetails
# Create your views here.


class CustomerAPI(APIView):
    def get(self,request):
        try:
            lst_customer_data = []
            if request.GET.get('id'):
                pass
            else:
                lst_customer_data = UserDetails.objects.filter(int_type = 3,user__is_active = True).values('user__first_name','user__last_name','phone_number','alt_phone_number','user__email','address','user')
                return Response({'data':lst_customer_data},status = HTTP_200_OK)
        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self,request):
        try:
            with transaction.atomic():
                if not request.data.get('first_name'):
                    raise Exception('First name is required')
                if not request.data.get('last_name'):
                    raise Exception('Last name is required')
                if not request.data.get('address'):
                    raise Exception('Address is required')
                if not request.data.get('Phone_number'):
                    raise Exception('Phone number is required')
                if not len(str(request.data.get('Phone_number'))) ==10 or request.data.get('alt_phone_number') == "":
                    raise Exception('Contact number must be 10 digit')
                if request.data.get('alt_phone_number') and not len(str(request.data.get('contact_no_alternate'))) ==10 or request.data.get('alt_phone_number') == "":
                    raise Exception('Alternate contact number must be 10 digit')
                if not request.data.get('email'):
                    raise Exception('Email is required')
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', request.data.get('email')):
                    raise Exception("Invalid email address")
                if not request.data.get('role_id'):
                    raise Exception('Role is required')
                if User.objects.filter(email = request.data.get('email'),is_active = True).exists():
                    raise Exception('Email already exist')

                user = User.objects.create(
                    first_name=request.data.get('first_name'),
                    last_name=request.data.get('last_name'),
                    email=request.data.get('email'),
                    username = request.data.get('email')
                )
                random_number = random.randint(1000, 9999)
                password = request.data.get('email') + str(random_number)
                user.set_password(password)

                UserDetails.objects.create(address = request.data.get('address'),
                                    phone_number = request.data.get('Phone_number'),
                                    alt_phone_number = request.data.get('alt_phone_number'),
                                    fk_role_id = request.data.get('role_id'),
                                    int_type = 3,
                                    user = user)

                return Response({"Message": "Customer created successfully"}, status=HTTP_201_CREATED)

        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self,request):
        try:
            if request.data.get('id') and User.objects.filter(id = request.data.get('id'),is_active = True).exists():
                with transaction.atomic():
                    if not request.data.get('first_name'):
                        raise Exception('First name is required')
                    if not request.data.get('last_name'):
                        raise Exception('Last name is required')
                    if not request.data.get('address'):
                        raise Exception('Address is required')
                    if not request.data.get('Phone_number'):
                        raise Exception('Phone number is required')
                    if not len(str(request.data.get('Phone_number'))) ==10 or request.data.get('alt_phone_number') == "":
                        raise Exception('Contact number must be 10 digit')
                    if request.data.get('alt_phone_number') and not len(str(request.data.get('contact_no_alternate'))) ==10 or request.data.get('alt_phone_number') == "":
                        raise Exception('Alternate contact number must be 10 digit')
                    if not request.data.get('email'):
                        raise Exception('Email is required')
                    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', request.data.get('email')):
                        raise Exception("Invalid email address")
                    if not request.data.get('role_id'):
                        raise Exception('Role is required')
                    if User.objects.filter(email = request.data.get('email'),is_active = True).exclude(id = request.data.get('id')).exists():
                        raise Exception('Email already exist')
                    user = User.objects.filter(id = request.data.get('id')).update(
                        first_name=request.data.get('first_name'),
                        last_name=request.data.get('last_name'),
                        email=request.data.get('email'),
                    )
                    UserDetails.objects.filter(user = request.data.get('id')).update(address = request.data.get('address'),
                                        phone_number = request.data.get('Phone_number'),
                                        alt_phone_number = request.data.get('alt_phone_number'),
                                        fk_role_id = request.data.get('role_id')
                                        )
                    return Response({"Message": "Customer updated successfully"}, status=HTTP_200_OK)
            else:
                raise Exception('Customer not found')
        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request):
        try:
            with transaction.atomic():
                if request.data.get('id') and User.objects.filter(id = request.data.get('id')).exists():
                    UserDetails.objects.filter(user = request.data.get('id'),is_active = True).delete()
                    user.objects.filter(id = request.data.get('id')).delete()
                    return Response({"Message": "Customer deleted successfully"}, status=HTTP_200_OK)
                else:
                    raise Exception('Customer not found')
        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)


        