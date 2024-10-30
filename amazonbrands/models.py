from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    # categories = models.CharField()

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    asin = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    image = models.URLField()
