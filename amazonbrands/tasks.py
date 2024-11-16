# amazonbrands/tasks.py
from celery import shared_task
from .models import Brand, Product
from amazonbrands.scraper import scrape_amazon_product_list


@shared_task
def scrape_amazon_products_for_all_brands():
    """
    Task to scrape Amazon products for each brand in the database.
    """
    # Retrieve all brands
    brand_names = Brand.objects.values_list('name', flat=True)

    for brand_name in brand_names:
        # Call a helper function to scrape products for the specific brand
        scrape_amazon_products(brand_name)

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
                image=product.get('image_url'),
                brand=brand
            )
            new_product.save()