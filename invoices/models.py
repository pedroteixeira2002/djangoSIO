from django.db import models
from datetime import datetime
from customers.models import Customer


class Payment(models.Model):
    payment_ref_no = models.CharField(primary_key=True, max_length=20)
    payment_mechanism = models.CharField(max_length=10)


# Create your models here.
class Invoice(models.Model):
    no = models.CharField(max_length=60, primary_key=True)
    type = models.CharField(max_length=2)
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    gross_total = models.FloatField()
    tax_payable = models.FloatField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)

    def set_date(self, date_str):
        self.date = datetime.strptime(date_str, '%Y-%m-$d').date()

