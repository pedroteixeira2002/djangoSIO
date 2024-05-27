from datetime import datetime

from django.db import models

from customers.models import Customer


# Create your models here.
class BuyOrder(models.Model):
    number = models.CharField(max_length=30, unique=True, primary_key=True)
    date = models.DateField()
    tipo = models.CharField(max_length=2)

    def set_date(self, date_str):
        self.date = datetime.strptime(date_str, '%Y-%m-$d').date()
