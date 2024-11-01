from django.urls import path
from . import views

urlpatterns = [
    path('', views.brands_list, name='brands_list'),
    path('<str:brand_name>', views.products_list, name='products_list'),
    path('test', views.test, name='test')
]