from django.urls import path

from invoice_lines import views

urlpatterns = [
    path('', views.product_count, name="Get Product Count For Invoice"),
]
