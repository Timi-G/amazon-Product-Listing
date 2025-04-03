# amazonbrands/tasks.py
import logging

from celery import shared_task
from .models import Brand, Product
from amazonbrands.scraper import scrape_amazon_products


logger = logging.getLogger(__name__)

@shared_task
def scrape_amazon_products_for_all_brands_db():
    """
    Task to scrape Amazon products for each brand in the database.
    """
    from django.db import close_old_connections
    close_old_connections()

    # Retrieve all brands
    brand_names = Brand.objects.values_list('name', flat=True)
    logger.info(f"Starting scrape for {len(brand_names)} brands")

    for brand_name in brand_names:
        logger.info(f"Scraping brand: {brand_name}")
        # Call a helper function to scrape products for the specific brand
        scrape_amazon_products(brand_name)

def save_amazon_brand_container(container, brand_name, products):
    brands = container
    if brand_name not in brands:
        brands[brand_name]=products
