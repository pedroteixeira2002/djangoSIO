from rest_framework import serializers

from invoice_lines.models import InvoiceLines


class InvoiceLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLines
        fields = ('id', 'product_code', 'quantity', 'unit_price', 'credit_amount')
