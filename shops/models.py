import uuid
from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    public_access = models.BooleanField(default=False)
    shop_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    shop_description = models.TextField()
    shop_creates_name = models.CharField(max_length=50)
    access_name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    access_password = models.CharField(max_length=255, blank=True, null=True)
    currency_name = models.CharField(max_length=255)
    currency_amount = models.PositiveIntegerField(blank=True, null=True)


class Product(models.Model):
    shop = models.ForeignKey(Shop, models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='shop_images', default='shop_images/defaultImage.png')
    product_name = models.CharField(max_length=100)
    product_description = models.TextField(max_length=500)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    product_amount = models.IntegerField(default=1)
    message_after_purchase = models.TextField(default='Access')
