# amazonbrands/tasks.py
from celery import shared_task
from .models import Brand, Product
from amazonbrands.scraper import scrape_amazon_products


@shared_task
def scrape_amazon_products_for_all_brands_db():
    """
    Task to scrape Amazon products for each brand in the database.
    """
    # Retrieve all brands
    brand_names = Brand.objects.values_list('name', flat=True)

    for brand_name in brand_names:
        # Call a helper function to scrape products for the specific brand
        scrape_amazon_products(brand_name)

def save_amazon_brand_container(container, brand_name, products):
    brands = container
    if brand_name not in brands:
        brands[brand_name]=products
