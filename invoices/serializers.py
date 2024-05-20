from rest_framework import serializers

from invoice_lines.serializers import InvoiceLinesSerializer
from invoices.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_lines = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ('no', 'type', 'date', 'customer', 'invoice_lines')

    def get_invoice_lines(self, obj):
        invoice_lines = obj.invoicelines_set.all()
        serializer = InvoiceLinesSerializer(invoice_lines, many=True)
        return serializer.data
