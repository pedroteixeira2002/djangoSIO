from django.db import models


# Create your models here.
class Product(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description
