from django.urls import path
from . import views

urlpatterns = [
    path('', views.brands_list, name='brands_list'),
    path('products/<str:brand_name>', views.products_list, name='products_list'),
    path('products', views.products_search, name='products_search'),
    path('test', views.test, name='test')
]
