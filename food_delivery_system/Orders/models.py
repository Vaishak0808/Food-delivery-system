from django.db import models
from login.models import UserDetails
from food.models import FoodProduct
from django.contrib.auth.models import User

class OrderStatus(models.Model):
    vchr_status = models.CharField(max_length = 30)
    def __str__(self):
        return self.vchr_status

# Create your models here.
class OrderMaster(models.Model):
    vchr_order_num = models.CharField(max_length= 50,null=True)
    fk_customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name = "customer_details")
    dat_created = models.DateTimeField(blank=True, auto_now = True)
    dat_updated =  models.DateTimeField(blank = True,null=True)
    fk_updated = models.ForeignKey(User,on_delete=models.CASCADE,related_name="updated_id",null=True,default=None)
    dbl_total_amount = models.FloatField()
    fk_order_status = models.ForeignKey(OrderStatus,on_delete=models.CASCADE,null=True)
    fk_delivery_agent = models.ForeignKey(User,on_delete=models.CASCADE,related_name = "agent_details",null=True,default=None)
    int_status = models.IntegerField(null = True ,blank=True) #1.ACTIVE 0.CANCELLED
    def __str__(self):
        return self.vchr_order_num
    
class OrderDetails(models.Model):
    fk_order = models.ForeignKey(OrderMaster,on_delete=models.CASCADE)
    fk_product = models.ForeignKey(FoodProduct,on_delete=models.CASCADE,null =True)
    int_status = models.IntegerField()  #1. ACTIVE 0.CANCELLED
    dbl_rate = models.FloatField()
    int_qty = models.IntegerField(blank=True)

