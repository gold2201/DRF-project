from datetime import timedelta
from django.utils import timezone

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.models import Shop
from shops.serializers import ShopSerializer

class PublicShopsListView(APIView):
    def get(self, request):
        filter_by = request.query_params.get('filter_by', None)

        if filter_by == 'today':
            today = timezone.now().date()
            shops = Shop.objects.filter(public_access=True, created_at__date=today)
        elif filter_by == 'week':
            week = timezone.now().date() - timedelta(days=7)
            shops = Shop.objects.filter(public_access=True, created_at__gte=week)
        elif filter_by:
            shops = Shop.objects.filter(public_access=True, shop_name=filter_by)
        else:
            shops = Shop.objects.filter(public_access=True)

        serializer = ShopSerializer(shops, many=True, fields = ['shop_name', 'public_access', 'shop_creates_name'])
        return Response(serializer.data, status=status.HTTP_200_OK)

class PublicShopDetailView(APIView):
    def get(self, request, uuid):
        shop = get_object_or_404(Shop, uuid=uuid)
        if not shop.public_access:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShopSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)

