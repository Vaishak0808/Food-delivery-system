from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=100)    
    code = models.CharField(max_length = 5)

    def __str__(self):
        return self.name


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(default=None)
    phone_number = models.IntegerField()
    alt_phone_number = models.IntegerField(null =True,default=None)
    fk_role = models.ForeignKey(Role,on_delete=models.CASCADE)
    int_type = models.IntegerField(null = True) #1.ADMIN 2.AGENT 3.CUSTOMER

    def __str__(self):
        return self.user.username

