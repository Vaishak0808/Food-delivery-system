from django.db import models

# Create your models here.


class FoodProduct(models.Model):
    name = models.TextField()
    amount = models.FloatField()
    def __str__(self):
        return self.name
