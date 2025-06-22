import logging

from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from shops.models import Shop, Product
from shops.serializers import ShopSerializer
from shops.services.shop_service import purchase_product, check_shop_object

logger = logging.getLogger(__name__)

class CreateViewShops(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Create new shop',
        description='Create a new shop after authentication',
        request=ShopSerializer,
        responses=ShopSerializer,
    )
    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.debug('Create shop triggered')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error('Error creating shop in CreateViewShops POST')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyShopsListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List all shops',
        description='List all shops owned by a user',
        request=ShopSerializer,
    )
    def get(self, request):
        user = request.user
        shops = Shop.objects.filter(user=user)
        serializer = ShopSerializer(shops, many=True, fields=('shop_name', 'public_access', 'shop_creates_name', 'uuid'))
        logger.debug('List shops triggered')
        return Response(serializer.data)

class WorkWithShopView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get shop details',
        description='Get shop details about a shop owned by a user',
        request=ShopSerializer,
    )
    def get(self, request, pk):
        shop = check_shop_object(pk)
        serializer = ShopSerializer(shop)
        logger.debug('Get shop details triggered')
        return Response(serializer.data)

    @extend_schema(
        summary='Update shop details',
        description='Update shop details about a shop owned by a user',
        request=ShopSerializer,
        responses=ShopSerializer,
    )
    def put(self, request, pk):
        shop = check_shop_object(pk)
        serializer = ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug('Update shop triggered')
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error('Error creating shop in CreateViewShops POST')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Delete shop',
        description='Delete shop owned by a user',
    )
    def delete(self, request, pk):
        shop = check_shop_object(pk)
        shop.delete()
        logger.debug('Delete shop triggered')
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Delete product in specific shop',
        description='Delete product in specific shop owned by a user',
    )
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        logger.debug('Delete product triggered')
        return Response(status=status.HTTP_204_NO_CONTENT)

class AccessedPrivateShopView(APIView):

    @extend_schema(
        summary='Authorization to the private shop',
        description='Authorization to private shop',
        responses=ShopSerializer,
    )
    def post(self, request):
        try:
            shop = Shop.objects.get(access_name=request.data['access_name'])
        except Shop.DoesNotExist:
            logger.critical('Failed to log in to the shop - AccessedPrivateShopView')
            return Response({'error': 'Invalid password or name'}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(request.data['access_password'], shop.access_password):
            serializer = ShopSerializer(shop)
            logger.debug('Authorization to the shop triggered')
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.critical('Failed to log in to the shop - AccessedPrivateShopView')
            return Response({'error': 'Invalid password or name'}, status=status.HTTP_400_BAD_REQUEST)

class WorkWithAccessedShopView(APIView):

    @extend_schema(
        summary='Get shop details',
        description='Get shop details about a shop after authorization in it',
        request=ShopSerializer,
    )
    def get(self, request, uuid):
        shop = get_object_or_404(Shop, uuid=uuid)
        serializer = ShopSerializer(shop)
        logger.debug('Get authorized shop triggered')
        return Response(serializer.data)

    @extend_schema(
        summary='Making a purchase decision',
        description='Making a purchase decision in private shop',
    )
    def put(self, request, uuid, pk):
        shop = get_object_or_404(Shop, uuid=uuid)
        product = get_object_or_404(Product, pk=pk)

        access, message = purchase_product(shop, product)
        if access:
            logger.debug('Making a purchase decision triggered')
            return Response(message, status=status.HTTP_200_OK)
        else:
            logger.error('Not enough money')
            return Response({'error': message}, status=status.HTTP_402_PAYMENT_REQUIRED)
