from django.db import models

from invoices.models import Invoice
from products.models import Product


# Create your models here.
class InvoiceLines(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_no = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product_code = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=19, decimal_places=10)
    unit_price = models.DecimalField(max_digits=19, decimal_places=10)
    credit_amount = models.FloatField()

    def __str__(self):
        return self.invoice_no.no
