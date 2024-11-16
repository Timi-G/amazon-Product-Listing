from django.contrib import admin
from django.contrib import messages
from celery import signals

from .models import Brand
from .models import Product
from amazonbrands.scraper import scrape_amazon_product_list
from amazonbrands.tasks import scrape_amazon_products


# Register your models here.
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    actions = ['scrape_products']

    def scrape_products(self, request, queryset):
        """
        Custom admin action to scrape products for selected brands.
        """
        for brand in queryset:
            # Trigger the scraping task for each selected brand

            self.message_user(request, f"Started scraping products for brand: {brand.name}", messages.INFO)
            scrape_amazon_product_list(brand.name)
            self.message_user(request, f"Finished scraping products for brand: {brand.name}", messages.INFO)
    scrape_products.short_description = "Scrape products for selected brands"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'asin', 'page', 'brand']

# Task success handler
@signals.task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    """
    Handle successful completion of a task and send a message to the user.
    """
    if result:
        from django.contrib.sessions.models import Session
        from django.contrib.auth.models import User

        session = Session.objects.get(pk=kwargs["task_id"])
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(id=user_id)

        # Send a success message to the user's session (Django message system)
        messages.add_message(user, messages.SUCCESS, result)
