from django.urls import path,include
from food.views import FoodAPI

urlpatterns = [
    path('food_product/',FoodAPI.as_view()),
    ]