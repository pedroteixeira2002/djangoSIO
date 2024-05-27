from django.urls import path

from customers import views

urlpatterns = [
    path('', views.customers_count, name="Get Total Clients"),
    path('customers_list/', views.customers_list, name="Get List Clients"),
    path('mostBoughtByClient/', views.customers_best_products, name="Customers best products")
]
