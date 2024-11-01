from django.shortcuts import render

from .models import Brand, Product

# Create your views here.
def products_list(request, brand_name):
    products = Product.objects.filter(brand__iexact=brand_name)
    return render(request, 'products.html', {'products': products})

def brands_list(request):
    brands = Brand.objects.all
    return render(request, 'brands.html', {'brands': brands})

def test(request):
    return render(request,'test.html')