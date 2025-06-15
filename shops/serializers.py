from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from shops.models import User, Shop, Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ['username', 'password']

    def validate(self, data):
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['shop']

class ShopSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Shop
        fields = ['shop_name', 'public_access','shop_description', 'shop_creates_name' ,'products']

    def create(self, validated_data):
        product_data = validated_data.pop('products')
        shop = Shop.objects.create(**validated_data)

        for product in product_data:
            Product.objects.create(shop=shop, **product)

        return shop

