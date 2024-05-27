from django.db import models


# Create your models here.
class TimeDimension(models.Model):
    date = models.DateField()
    sk_year_month = models.CharField(primary_key=True, unique=True, max_length=150, blank=True)

    def save(self, *args, **kwargs):
        self.sk_year_month = f"{self.date.year}_{self.date.month}"
        existing_object = TimeDimension.objects.filter(sk_year_month=self.sk_year_month).first()

        if not existing_object:
            super().save(*args, **kwargs)
