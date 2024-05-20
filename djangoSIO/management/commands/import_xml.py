import os
from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET

from products.models import Product
from customers.models import Address, Customer
from invoices.models import Invoice, Payment
from invoice_lines.models import InvoiceLines


class Command(BaseCommand):
    help = 'Import data from XML file to database'

    def handle(self, *args, **options):
        xml_file_path = os.path.join(os.getcwd(), 'saft.xml')
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        namespace = root.tag.split('}')[0] + '}'

        products = root.findall('.//{0}Product'.format(namespace))
        save_products(products, namespace)

        customers = root.findall('.//{0}Customer'.format(namespace))
        save_customers(customers, namespace)

        invoices = root.findall('.//{0}Invoice'.format(namespace))
        save_invoices(invoices, namespace)

        payments = root.findall('.//{0}Payments/{0}Payment'.format(namespace))
        payments_save(payments, namespace)


def payments_save(payments, namespace):
    for payment in payments:
        payment_lines = payment.findall('.//{0}Line'.format(namespace))
        payment_ref = payment.find('{0}PaymentRefNo'.format(namespace)).text
        payment_method = payment.find('{0}PaymentMethod/{0}PaymentMechanism'.format(namespace)).text
        payment = Payment.objects.get_or_create(payment_ref_no=payment_ref, payment_mechanism=payment_method)
        for payment_line in payment_lines:
            invoice_no = payment_line.find('{0}SourceDocumentID/{0}OriginatingON'.format(namespace)).text
            invoice = Invoice.objects.get(no=invoice_no)

            invoice.payment = payment[0]
            invoice.save()


def save_invoices(invoices, namespace):
    for invoice in invoices:
        invoice_no = invoice.find('{0}InvoiceNo'.format(namespace)).text
        invoice_type = invoice.find('{0}InvoiceType'.format(namespace)).text
        invoice_date = invoice.find('{0}InvoiceDate'.format(namespace)).text
        invoice_gross_total = invoice.find('{0}DocumentTotals/{0}GrossTotal'.format(namespace)).text
        invoice_tax_payable = invoice.find('{0}DocumentTotals/{0}TaxPayable'.format(namespace)).text
        customer_id = invoice.find('{0}CustomerID'.format(namespace)).text
        customer = Customer.objects.get(id=customer_id)

        invoice_to_create = Invoice(no=invoice_no, type=invoice_type, date=invoice_date,
                                    gross_total=invoice_gross_total, tax_payable=invoice_tax_payable)
        invoice_to_create.customer = customer
        invoice_to_create.save()

        invoice_lines = invoice.findall('{0}Line'.format(namespace))
        save_invoices_lines(invoice_lines, namespace, invoice_to_create)


def save_invoices_lines(invoices_lines, namespace, invoice):
    for invoices_line in invoices_lines:
        product_code = invoices_line.find('{0}ProductCode'.format(namespace)).text
        quantity = invoices_line.find('{0}Quantity'.format(namespace)).text
        unit_price = invoices_line.find('{0}UnitPrice'.format(namespace)).text
        credit_amount = invoices_line.find('{0}CreditAmount'.format(namespace)).text

        product_code = Product.objects.get(code=product_code)
        invoices_line_to_add = InvoiceLines(quantity=quantity, unit_price=unit_price, credit_amount=credit_amount)
        invoices_line_to_add.invoice_no = invoice
        invoices_line_to_add.product_code = product_code
        invoices_line_to_add.save()


def save_customers(customers, namespace):
    for customer in customers:
        billing_address = customer.find('{0}BillingAddress/{0}AddressDetail'.format(namespace)).text
        city = customer.find('{0}BillingAddress/{0}City'.format(namespace)).text
        postal_code = customer.find('{0}BillingAddress/{0}PostalCode'.format(namespace)).text
        country = customer.find('{0}BillingAddress/{0}Country'.format(namespace)).text
        address, _ = Address.objects.get_or_create(detail=billing_address, city=city, postal_code=postal_code,
                                                   country=country)

        id = customer.find('{0}CustomerID'.format(namespace)).text
        account_id = customer.find('{0}AccountID'.format(namespace)).text
        customer_tax_id = customer.find('{0}CustomerTaxID'.format(namespace)).text
        company_name = customer.find('{0}CompanyName'.format(namespace)).text
        customer_to_add = Customer(id=id, account_id=account_id, tax_id=customer_tax_id,
                                   company_name=company_name)
        customer_to_add.address = address
        customer_to_add.save()


def save_products(products, namespace):
    for product in products:
        code = product.find('{0}ProductCode'.format(namespace)).text

        description = product.find('{0}ProductDescription'.format(namespace)).text

        product_to_add = Product(code=code, description=description)
        product_to_add.save()
