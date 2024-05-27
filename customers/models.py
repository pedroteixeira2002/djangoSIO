from django.db import models


class Address(models.Model):
    class Meta:
        unique_together = (('detail', 'postal_code'),)

    detail = models.CharField(max_length=210)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=12)

    def __str__(self):
        return self.detail


# Create your models here.

class Customer(models.Model):
    # nif = models.IntegerField(max_length=9, unique=True)
    id = models.CharField(max_length=30, primary_key=True)
    account_id = models.CharField(max_length=30)
    tax_id = models.CharField(max_length=30)
    company_name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name
