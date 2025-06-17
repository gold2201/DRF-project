from django.contrib.auth.hashers import make_password
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
        fields = ['uuid', 'shop_name', 'public_access','shop_description', 'shop_creates_name', 'created_at', 'access_name',
                  'access_password','currency_name','currency_amount', 'products']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)

            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def create_helper(self, validated_data):
        product_data = validated_data.pop('products')
        shop = Shop.objects.create(**validated_data)

        for product in product_data:
            Product.objects.create(shop=shop, **product)

        return shop

    def create(self, validated_data):
        if validated_data['public_access']:
            if validated_data.get('access_name') or validated_data.get('access_password') or validated_data.get('currency_amount'):
                raise serializers.ValidationError('Public store should not contain password, access name and currency amount')
            return self.create_helper(validated_data)
        else:
            validated_data['access_password'] = make_password(validated_data['access_password'])
            return self.create_helper(validated_data)
