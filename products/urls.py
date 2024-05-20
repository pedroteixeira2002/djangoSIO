from django.urls import path
from . import views
urlpatterns = [
    path('', views.get_all_products, name="Get All Products"),
]
