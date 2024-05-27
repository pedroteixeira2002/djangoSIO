from django.db.models import Sum
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from invoice_lines.models import InvoiceLines
from products.models import Product
from .models import Customer


# Create your views here.
@api_view(['GET'])
def customers_count(request):
    response = {}
    total_clients = Customer.objects.count()
    response["total_clients"] = total_clients
    return JsonResponse(response)


@api_view(['GET'])
def customers_list(request):
    customers = Customer.objects.all()
    customer_data = []

    for customer in customers:
        customer_data.append({
            'customer_id': customer.id,
            'company_name': customer.company_name,
            # Adicione mais campos conforme necessário
        })

    return JsonResponse(customer_data, safe=False)


@api_view(['GET'])
def customers_best_products(request):
    customers = Customer.objects.all()
    most_bought_products = []

    for customer in customers:
        product_quantity = (
            InvoiceLines.objects
            .filter(invoice_no__customer=customer)
            .values('product_code')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity')
            .first()
        )

        if product_quantity:
            product = Product.objects.get(code=product_quantity['product_code'])
            most_bought_products.append({
                'customer_id': customer.id,
                'customer_name': customer.company_name,
                'most_bought_product': product.description,
            })

    return Response(most_bought_products)
