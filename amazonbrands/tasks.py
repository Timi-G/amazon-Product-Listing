# amazonbrands/tasks.py
from celery import shared_task
from .models import Brand, Product
from amazonbrands.scraper import scrape_amazon_product_list

@shared_task
def scrape_amazon_products(brand_name):
    products = scrape_amazon_product_list(brand_name)
    brand, created = Brand.objects.get_or_create(name=brand_name)
    for product in products:
        # Save the product data to the database or take any required action
        asin = product.get('asin')

        # Check if a product with this ASIN already exists
        if not Product.objects.filter(asin=asin, brand=brand).exists():
            # If it doesn't exist, create a new product entry
            new_product=Product.objects.create(
                name=product.get('name'),
                asin=asin,
                page=product.get('page'),
                image_url=product.get('image_url'),
                brand=brand
            )
            new_product.save()
        print(product)

if __name__ == "__main__":
    import sys
    brand_name = sys.argv[1]
    scrape_amazon_products(brand_name)
