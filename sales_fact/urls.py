from django.urls import path

from . import views

urlpatterns = [
    path('<str:year_month>', views.get_net_value_by_year_and_month, name="Get All Invoices"),

]
