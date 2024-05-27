import calendar

from django.db.models import Sum, Count
from django.db.models.functions import ExtractIsoWeekDay
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from customers.models import Customer
from invoices.models import Invoice
from invoices.serializers import InvoiceSerializer


# Create your views here.
@api_view(['GET'])
def get_all_invoices(request, year):
    invoices = Invoice.objects.filter(date__year=year)
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_sales_by_month(request, year):
    counts = {}
    labels = []
    values = []

    for month in range(1, 13):
        count = Invoice.objects.filter(date__year=year, date__month=month).count()
        labels.append(calendar.month_name[month])
        values.append(count)

    counts["labels"] = labels
    counts["values"] = values
    return JsonResponse(counts)


@api_view(['GET'])
def customer_gross_total(request, year):
    totals = Invoice.objects.values('customer').annotate(gross_total_sum=Sum('gross_total'))

    result = []
    for total in totals:
        customer_id = total['customer']
        customer = Customer.objects.get(id=customer_id)
        gross_total_sum = total['gross_total_sum']

        if year:  # Filtra os totais brutos pelo ano, se fornecido
            invoices = Invoice.objects.filter(customer=customer_id, date__year=year)
            gross_total_sum = invoices.aggregate(sum_gross=Sum('gross_total'))['sum_gross']

        customer_data = {
            'customer_id': customer_id,
            'customer_name': customer.company_name,
            'gross_total_sum': gross_total_sum
        }
        result.append(customer_data)

    return JsonResponse(result, safe=False)


@api_view(['GET'])
def get_gross_total_by_month(request, year):
    counts = {}
    labels = []
    values = []

    for month in range(1, 13):
        total = Invoice.objects.filter(date__year=year, date__month=month).aggregate(Sum('gross_total'))
        labels.append(calendar.month_name[month])
        values.append(total['gross_total__sum'] or 0)

    counts["labels"] = labels
    counts["values"] = values
    return JsonResponse(counts)


@api_view(['GET'])
def get_most_used_payment_methods(request, year):
    invoices = Invoice.objects.exclude(payment__isnull=True)

    if year:  # Filtra as faturas pelo ano, se fornecido
        invoices = invoices.filter(date__year=year)

    payment_mechanisms = invoices.values_list('payment__payment_mechanism', flat=True)
    payment_mechanism_counts = {}

    for mechanism in payment_mechanisms:
        if mechanism in payment_mechanism_counts:
            payment_mechanism_counts[mechanism] += 1
        else:
            payment_mechanism_counts[mechanism] = 1

    labels = list(payment_mechanism_counts.keys())
    values = list(payment_mechanism_counts.values())

    data = {
        'labels': labels,
        'values': values
    }

    return Response(data)


@api_view(['GET'])
def get_sales_by_week_day(request, year):
    weekday_counts = Invoice.objects.annotate(weekday=ExtractIsoWeekDay('date')).values('weekday').annotate(
        count=Count('weekday')).order_by('weekday')

    weekday_labels = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday'
    }

    labels = []
    values = []

    for weekday in range(1, 8):
        weekday_label = weekday_labels.get(weekday, 'Unknown')
        labels.append(weekday_label)

        count = next((entry['count'] for entry in weekday_counts if entry['weekday'] == weekday), 0)
        values.append(count)

    data = {
        'labels': labels,
        'values': values
    }

    return Response(data)


@api_view(['GET'])
def get_sales_for_city(request, year):
    invoice_count = (
        Invoice.objects
        .values('customer__address__city')
        .annotate(count=Count('no'))
    )

    labels = []
    values = []

    for item in invoice_count:
        city = item['customer__address__city']
        count = item['count']
        labels.append(city)
        values.append(count)

    result = {
        'labels': labels,
        'invoice_counts': values
    }

    return Response(result)


@api_view(['GET'])
def count_sales_for_foreign(request, year):
    total_invoices = Invoice.objects.count()

    invoice_count = (
        Invoice.objects
        .exclude(customer__address__country='PT')
        .values('customer__address__country')
        .annotate(count=Count('no'))
    )

    total_invoice_count = 0
    for item in invoice_count:
        total_invoice_count += item['count']

    result = {
        'foreign_percentage': total_invoice_count / total_invoices
    }

    return Response(result)


@api_view(['GET'])
def total_tax_payed(request, year):
    total_tax_payable = Invoice.objects.aggregate(sum_tax=Sum('tax_payable'))['sum_tax']

    result = {
        'total_tax_payable': total_tax_payable
    }

    return Response(result)


@api_view(['GET'])
def get_sales_by_week_day(request, year):
    weekday_counts = Invoice.objects.filter(date__year=year).annotate(weekday=ExtractIsoWeekDay('date')).values(
        'weekday').annotate(
        count=Count('weekday')).order_by('weekday')

    weekday_labels = {
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday',
        7: 'Sunday'
    }

    labels = []
    values = []

    for weekday in range(1, 8):
        weekday_label = weekday_labels.get(weekday, 'Unknown')
        labels.append(weekday_label)

        count = next((entry['count'] for entry in weekday_counts if entry['weekday'] == weekday), 0)
        values.append(count)

    data = {
        'labels': labels,
        'values': values
    }

    return Response(data)


@api_view(['GET'])
def get_sales_for_city(request, year):
    invoice_count = (
        Invoice.objects.filter(date__year=year)  # Filtra as faturas pelo ano, se fornecido
        .values('customer__address__city')
        .annotate(count=Count('no'))
    )

    labels = []
    values = []

    for item in invoice_count:
        city = item['customer__address__city']
        count = item['count']
        labels.append(city)
        values.append(count)

    result = {
        'labels': labels,
        'invoice_counts': values
    }

    return Response(result)


@api_view(['GET'])
def count_sales_for_foreign(request, year):
    total_invoices = Invoice.objects.filter(date__year=year).count()

    invoice_count = (
        Invoice.objects
        .exclude(customer__address__country='PT')
        .filter(date__year=year)  # Filtra as faturas pelo ano, se fornecido
        .values('customer__address__country')
        .annotate(count=Count('no'))
    )

    total_invoice_count = 0
    for item in invoice_count:
        total_invoice_count += item['count']

    result = {
        'foreign_percentage': total_invoice_count / total_invoices
    }

    return Response(result)


@api_view(['GET'])
def total_tax_payed(request, year):
    total_tax_payable = Invoice.objects.filter(date__year=year).aggregate(sum_tax=Sum('tax_payable'))['sum_tax']

    result = {
        'total_tax_payable': total_tax_payable
    }

    return Response(result)
