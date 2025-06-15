from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    public_access = models.BooleanField(default=False)
    shop_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    shop_description = models.CharField(max_length=255)
    shop_creates_name = models.CharField(max_length=50)

class Product(models.Model):
    shop = models.ForeignKey(Shop, models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='shop_images', default='shop_images/defaultImage.png')
    product_name = models.CharField(max_length=100)
    product_description = models.TextField(max_length=500)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    product_amount = models.IntegerField(default=1)


# Create your models here.
