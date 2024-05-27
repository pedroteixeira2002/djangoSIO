import calendar

from django.db.models import Count
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import InvoiceLines


# Create your views here.
@api_view(['GET'])
def product_count(request):
    counts = InvoiceLines.objects.values('invoice_no__date__month', 'product_code__description').annotate(
        count=Count('product_code')).order_by('invoice_no__date__month')
    result = []
    current_month = None
    current_data = None
    for count in counts:
        month = count['invoice_no__date__month']
        description = count['product_code__description']
        count_data = {
            'description': description,
            'count': count['count']
        }
        if month != current_month:
            current_month = month
            current_data = {
                str(calendar.month_name[month]): [count_data]
            }
            result.append(current_data)
        else:
            current_data[str(calendar.month_name[month])].append(count_data)
    return JsonResponse(result, safe=False)
