# Create your models here.
from django.db import models

from time_dimension.models import TimeDimension


# Create your models here.
class SalesFact(models.Model):
    sk = models.ForeignKey(
        TimeDimension, related_name='sk_year_month_fact', db_column='sk_year_month', on_delete=models.CASCADE,
        null=False)
    net_total = models.FloatField(null=False)
