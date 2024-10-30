# amazonbrands/tasks.py
from celery import shared_task
from .scraper import scrape_amazon_product_list

@shared_task
def scrape_amazon_products(brand_url):
    products = scrape_amazon_product_list(brand_url)
    for product in products:
        # Save the product data to the database or take any required action
        print(product)
