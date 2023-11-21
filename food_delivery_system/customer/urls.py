from django.urls import path,include
from customer.views import CustomerAPI

urlpatterns = [
        path('customer_api/',CustomerAPI.as_view())

]