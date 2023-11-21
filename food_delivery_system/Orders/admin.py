from django.contrib import admin
from Orders.models import OrderMaster,OrderDetails,OrderStatus
# Register your models here.


class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['vchr_status']
admin.site.register(OrderStatus,OrderStatusAdmin)
class OrderMasterAdmin(admin.ModelAdmin):
    list_display = ['id','dat_created','get_customer','vchr_order_num','dbl_total_amount','fk_order_status','fk_delivery_agent','dat_updated']
    def get_customer(self,obj):
        return obj.fk_customer.first_name +' '+obj.fk_customer.last_name
admin.site.register(OrderMaster,OrderMasterAdmin)

class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['fk_order_id','def_order_num','fk_product_id','def_fk_product','dbl_rate','int_qty']
    def def_fk_product(self,obj):
        return obj.fk_product
    def def_order_num(self,obj):
        return obj.fk_order.vchr_order_num
admin.site.register(OrderDetails,OrderDetailsAdmin)