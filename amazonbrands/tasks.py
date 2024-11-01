# amazonbrands/tasks.py
from celery import shared_task
from .models import Product
from .scraper import scrape_amazon_product_list

@shared_task
def scrape_amazon_products(brand):
    products = scrape_amazon_product_list(brand)
    for product in products:
        # Save the product data to the database or take any required action
        asin = product.get('asin')

        # Check if a product with this ASIN already exists
        if not Product.objects.filter(asin=asin).exists():
            # If it doesn't exist, create a new product entry
            Product.objects.create(
                name=product.get('name'),
                asin=asin,
                page=product.get('page'),
                image_url=product.get('image_url')
            )
        print(product)
