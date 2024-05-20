from django.db import models
from datetime import datetime
from customers.models import Customer
from products.models import Product


# Create your models here.
class BuyOrderLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    net_value = models.FloatField()
    tax_percentage = models.IntegerField()
