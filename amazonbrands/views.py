from django.shortcuts import render

from .models import Brand, Product

# Create your views here.
def products_list(request, brand_name):
    brand_name=brand_name.capitalize()
    products = Product.objects.filter(brand__name=brand_name)

    return render(request, 'products.html', {'products': products, 'brand_name':brand_name})

def products_search(request):
    brand_name = request.GET.get('brand_name', '').strip().capitalize()
    products = []

    if brand_name:
        # Filter products by brand name
        products = Product.objects.filter(brand__name=brand_name)

    return render(request, 'products.html', {'products': products, 'brand_name':brand_name})

def brands_list(request):
    brands = Brand.objects.all
    return render(request, 'brands.html', {'brands': brands})

def test(request):
    return render(request,'test.html')