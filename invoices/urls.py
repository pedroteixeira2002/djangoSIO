from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_all_invoices, name="Get All Invoices"),
    path('getSalesByMonth/<int:year>/', views.get_sales_by_month, name="Get Invoices for year"),
    path('getGrossByMonth/<int:year>/', views.get_gross_total_by_month, name="Get Gross By Month"),
    path('customerGrossSale/<int:year>/', views.customer_gross_total, name="Get Gross By Customer"),
    path('mostPaymentMethods/<int:year>/', views.get_most_used_payment_methods, name="Get Most Payment Method"),
    path('salesByWeekDay/<int:year>/', views.get_sales_by_week_day, name="Sales By weekday"),
    path('salesByCity/<int:year>/', views.get_sales_for_city, name="Sales By city"),
    path('taxPayed/<int:year>/', views.total_tax_payed, name="Total Tax Payed"),
    path('percSalesForeign/<int:year>/', views.count_sales_for_foreign, name="Sales Foreign")
]
