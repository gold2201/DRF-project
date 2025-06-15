from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from shops.models import Shop
from shops.serializers import ShopSerializer

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
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)

class WorkWithShopView(APIView):
    permission_classes = [IsAuthenticated]

    def check_shop_object(self, pk):
        shop = get_object_or_404(Shop, pk=pk)
        return shop

    def get(self, request, pk):
        shop = self.check_shop_object(pk)
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    def put(self, request, pk):
        shop = self.check_shop_object(pk)
        serializer = ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        shop = self.check_shop_object(pk)
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)