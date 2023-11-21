from django.contrib import admin
from food.models import FoodProduct
# Register your models here.


class FoodProductAdmin(admin.ModelAdmin):
    list_display = ['id','name']
admin.site.register(FoodProduct,FoodProductAdmin)
