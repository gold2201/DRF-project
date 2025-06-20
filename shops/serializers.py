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
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'image', 'product_name', 'product_description',
                  'product_price', 'product_amount', 'message_after_purchase']

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

    def update(self, instance, validated_data):
        products = validated_data.pop('products', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if products:
            for product_data in products:
                if product_data.get('id', None):
                    try:
                        product = instance.products.get(id=product_data['id'])
                    except Product.DoesNotExist:
                        raise serializers.ValidationError(f'Product with id {product_data['id']} does not exist')
                    for attr, value in product_data.items():
                        setattr(product, attr, value)
                else:
                    product = instance.products.create(**product_data)
                product.save()
        return instance


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
            if not validated_data.get('access_name') or not validated_data.get('access_password') or not validated_data.get('currency_amount'):
                raise serializers.ValidationError('Private store should contain access password, access name and currency amount')
            validated_data['access_password'] = make_password(validated_data['access_password'])
            return self.create_helper(validated_data)
