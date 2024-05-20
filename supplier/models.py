from django.db import models


# Create your models here.
class Supplier(models.Model):
    nif = models.IntegerField(max_length=9)
    name = models.CharField(max_length=50)



    def __str__(self):
        return self.name
