from django.urls import path,include
from Orders.views import OrderAPI

urlpatterns = [
    path('place_order/',OrderAPI.as_view()),
]