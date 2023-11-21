from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_201_CREATED,HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_401_UNAUTHORIZED,HTTP_500_INTERNAL_SERVER_ERROR
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from Orders.models import OrderDetails,OrderMaster,OrderStatus
from login.models import UserDetails
from django.db.models import F, Value, CharField, ExpressionWrapper
from django.db.models.functions import Concat

# Create your views here.

class OrderAPI(APIView):
    def get(self,request):
        try:
            if request.user:
                ins_details = None
                ins_userDetails = UserDetails.objects.filter(id = request.user.id).first()
                if ins_userDetails and ins_userDetails.fk_role.name.upper() == "ADMIN":
                    ins_details = OrderDetails.objects.filter(fk_order__int_status = 1).annotate(customer=Concat('fk_order__fk_customer__first_name',Value(' '),'fk_order__fk_customer__last_name'),agent = Concat('fk_order__fk_delivery_agent__first_name',Value(' '),'fk_order__fk_delivery_agent__last_name')).values('agent','fk_product_id','fk_product__name','fk_order__vchr_order_num','customer','fk_order__dat_created','fk_order__fk_order_status__vchr_status','dbl_rate','int_qty','fk_order__dbl_total_amount')

                elif ins_userDetails and ins_userDetails.fk_role.name.upper() == "CUSTOMER":
                    ins_details = OrderDetails.objects.filter(fk_order__int_status = 1,fk_order__fk_customer_id = request.user.id).annotate(agent= Concat('fk_order__fk_delivery_agent__first_name',Value(' '),'fk_order__fk_delivery_agent__last_name')).values('agent','fk_product_id','fk_product__name','fk_order__vchr_order_num','fk_order__fk_customer','fk_order__dat_created','fk_order__fk_order_status__vchr_status','dbl_rate','int_qty','fk_order__dbl_total_amount')

                elif ins_userDetails and ins_userDetails.fk_role.name.upper() == "AGENT":
                    ins_details = OrderDetails.objects.filter(fk_order__int_status = 1,fk_order__fk_delivery_agent_id = request.user.id).annotate(customer=Concat('fk_order__fk_customer__first_name',Value(' '),'fk_order__fk_customer__last_name')).values('customer','fk_product_id','fk_product__name','fk_order__vchr_order_num','fk_order__fk_customer','fk_order__dat_created','fk_order__fk_order_status__vchr_status','dbl_rate','int_qty','fk_order__dbl_total_amount')
                    
                dct_data = {}
                for data in ins_details:
                    dct_line_level = {}
                    if data['fk_order__vchr_order_num'] not in dct_data:
                        dct_data[data['fk_order__vchr_order_num']] = {}
                        if data.get('customer'):
                            dct_data[data['fk_order__vchr_order_num']]['Customer'] = data['customer']
                        if data.get('agent'):
                            dct_data[data['fk_order__vchr_order_num']]['Agent'] = data['agent']
                        dct_data[data['fk_order__vchr_order_num']]['Total amount'] = data['fk_order__dbl_total_amount']
                        dct_data[data['fk_order__vchr_order_num']]['Order status'] = data['fk_order__fk_order_status__vchr_status']
                        dct_data[data['fk_order__vchr_order_num']]['Order date'] = data['fk_order__dat_created'].strftime("%Y-%m-%d %I:%M:%S %p")
                        dct_data[data['fk_order__vchr_order_num']]['Item details'] = []
                        dct_line_level['Product'] = data['fk_product__name']
                        dct_line_level['Quantity'] = data['int_qty']
                        dct_line_level['Unit Price'] = data['dbl_rate']
                        dct_data[data['fk_order__vchr_order_num']]['Item details'].append(dct_line_level)
                    else:
                        dct_line_level['Product'] = data['fk_product__name']
                        dct_line_level['Quantity'] = data['int_qty']
                        dct_line_level['Unit Price'] = data['dbl_rate']
                        dct_data[data['fk_order__vchr_order_num']]['Item details'].append(dct_line_level)
                return Response({'data':dct_data},status = HTTP_200_OK)
            return Response({'Message':"Permission denied"},status = HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self,request):
        try:
            with transaction.atomic():
                if request.data.get('data'):
                    dbl_total_amount = 0
                    int_id =  OrderMaster.objects.values('id').last()['id'] if  OrderMaster.objects.values('id').last() else 0
                    vchr_order_num = 'ORD-'+str(int_id + 1).zfill(4)
                    ins_order_master = OrderMaster(
                            fk_customer_id = request.user.id,
                            dat_created = datetime.now(),
                            vchr_order_num = vchr_order_num,
                            dbl_total_amount = 0,
                            fk_order_status_id = OrderStatus.objects.filter(vchr_status__icontains = "PENDING").values('id').first()['id'] if  OrderStatus.objects.filter(vchr_status__icontains = "PENDING").values('id').first() else None
                            )
                    ins_order_master.save()
                    
                    for index,items in enumerate(request.data.get('data')):
                        if items.get('fk_product_id') == "" or not items.get('fk_product_id'):
                            raise Exception('Enter item name for row '+str(index))
                        if items.get('int_qty') == "" or not items.get('int_qty'):
                            raise Exception('Enter quantity for row '+str(index))
                        
                        dbl_total_amount = dbl_total_amount + (items.get('dbl_rate') * items.get('int_qty'))
                        OrderDetails.objects.create(
                            fk_order = ins_order_master,
                            fk_product_id = items.get('fk_product_id'),
                            int_status = 1,
                            dbl_rate = items.get('dbl_rate'),
                            int_qty = items.get('int_qty')
                        )
                    if ins_order_master:
                        ins_order_master.dbl_total_amount = dbl_total_amount
                        ins_order_master.save()
                        
                    return Response({'Message':"Order placed successfully"},status = HTTP_201_CREATED)
                return Response({'Message':"Somthing went wrong"},status = HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self,request):
        try:
            with transaction.atomic():
                if request.data.get('id'):
                    ins_order_data =  OrderMaster.objects.filter(id = request.data.get('id')).first()
                    ins_userDetails = UserDetails.objects.filter(id = request.user.id).first()
                    if ins_order_data and ins_userDetails.fk_role.name.upper() == "ADMIN":
                        if ins_order_data.fk_order_status.vchr_status.upper() =="PENDING":
                            ins_order_data.fk_order_status =  OrderStatus.objects.filter(vchr_status = "ASSIGNED").first()
                            ins_order_data.fk_delivery_agent_id = request.data.get('agent_id')
                            ins_order_data.dat_updated = datetime.now()
                            ins_order_data.fk_updated_id = request.user.id
                            ins_order_data.save()
                            return Response({"Message":"Order assigned successfuly"},status = HTTP_200_OK)
                        if request.data.get('action') == 'CANCEL':
                            ins_order_data.fk_order_status = OrderStatus.objects.filter(vchr_status = "CANCELLED").first()
                            ins_order_data.int_status = 0
                            ins_order_data.dat_updated = datetime.now()
                            ins_order_data.fk_updated_id = request.user.id
                            ins_order_data.save()
                            return Response({"Message":"Order cancelled successfuly"},status = HTTP_200_OK)
                    if ins_order_data and ins_userDetails.fk_role.name.upper() == "AGENT" and ins_order_data.fk_order_status.upper() == "ASSIGNED":
                        ins_order_data.fk_order_status =  OrderStatus.objects.filter(vchr_status = "ASSIGNED").first()
                        ins_order_data.dat_updated = datetime.now()
                        ins_order_data.fk_updated_id = request.user.id
                        ins_order_data.save()
                        return Response({"Message":"Order delivered successfuly"},status = HTTP_200_OK)
                return Response({'Message':"Order not found"},status = HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Message":str(e)},status = HTTP_500_INTERNAL_SERVER_ERROR)