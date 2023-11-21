from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_201_CREATED,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR

from food.models import FoodProduct



class FoodAPI(APIView):
    def get(self,request):
        try:
            lst_food_data = []
            if request.GET.get('id'):
                lst_food_data = FoodProduct.objects.filter(id = request.GET.get('id')).values()
            else:
                lst_food_data = FoodProduct.objects.all().values('name','amount')

            return Response({'data':lst_food_data},status = HTTP_200_OK)
        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        try:
            if not request.data.get('name'):
                raise Exception('Item name is required')
            elif not request.data.get('amount'):
                raise Exception('Amount is required')
            else:
                FoodProduct.objects.create(name = request.data.get('name'),amount = request.data.get('amount'))
                return Response({'Message':'Item created successfully'},status = HTTP_201_CREATED)
        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self,request):
        try:
            if request.data.get('id') and FoodProduct.objects.filter(id =request.data.get('id')).exists():
                if not request.data.get('name'):
                    raise Exception('Item name is required')
                elif not request.data.get('amount'):
                    raise Exception('Amount is required')
                else:
                    FoodProduct.objects.filter(id = request.data.get('id')).update(name = request.data.get('name'),amount = request.data.get('amount'))
                    return Response({'Message':'Item updated successfully'},status = HTTP_201_CREATED)
            return Response(status = HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self,request):
        try:
            if request.data.get('id'):
                FoodProduct.objects.filter(id = request.GET.get('id')).delete()
                return Response({'Message':"Item deleted successfully"},status = HTTP_201_CREATED)
            return Response(status = HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)
