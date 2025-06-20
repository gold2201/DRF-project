from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from shops.models import Shop, Product
from shops.serializers import ShopSerializer
from shops.services.shop_service import purchase_product, check_shop_object

class CreateViewShops(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyShopsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        shops = Shop.objects.filter(user=user)
        serializer = ShopSerializer(shops, many=True, fields=('shop_name', 'public_access', 'shop_creates_name', 'uuid'))
        return Response(serializer.data)

class WorkWithShopView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        shop = check_shop_object(pk)
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def put(self, request, pk):
        shop = check_shop_object(pk)
        serializer = ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        shop = check_shop_object(pk)
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AccessedPrivateShopView(APIView):

    def post(self, request):
        try:
            shop = Shop.objects.get(access_name=request.data['access_name'])
        except Shop.DoesNotExist:
            return Response({'error': 'Invalid password or name'}, status=status.HTTP_400_BAD_REQUEST)

        if check_password(request.data['access_password'], shop.access_password):
            serializer = ShopSerializer(shop)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid password or name'}, status=status.HTTP_400_BAD_REQUEST)

class WorkWithAccessedShopView(APIView):

    def get(self, request, uuid):
        shop = get_object_or_404(Shop, uuid=uuid)
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def put(self, request, uuid, pk):
        shop = get_object_or_404(Shop, uuid=uuid)
        product = get_object_or_404(Product, pk=pk)

        access, message = purchase_product(shop, product)
        if access:
            return Response(message, status=status.HTTP_200_OK)
        else:
            return Response({'error': message}, status=status.HTTP_402_PAYMENT_REQUIRED)
