from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from sales_fact.models import SalesFact


# Create your views here.

@api_view(['GET'])
def get_net_value_by_year_and_month(request, year_month):
    sales_fact = get_object_or_404(SalesFact, sk=year_month)

    return Response({"net_total": sales_fact.net_total})
