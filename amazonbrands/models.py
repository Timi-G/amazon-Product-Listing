from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=200)
    # url = models.URLField()
    # categories = models.CharField()

    def __str__(self):
        return self.name

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_query_name="brand")
    name = models.CharField(max_length=200)
    asin = models.CharField(max_length=100)
    page = models.URLField(null=True)
    image = models.URLField()

    def __str__(self):
        return self.name
