import logging
from datetime import timedelta
from django.utils import timezone

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.models import Shop
from shops.serializers import ShopSerializer

logger = logging.getLogger(__name__)

class PublicShopsListView(APIView):
    @extend_schema(
        summary='Filter and found public shops',
        description='Filter public stores by days, name and display the entire list of public stores',
        responses=ShopSerializer,
    )
    def get(self, request):
        filter_by = request.query_params.get('filter_by', None)

        if filter_by == 'today':
            logger.debug('Today filter triggered')
            today = timezone.now().date()
            shops = Shop.objects.filter(public_access=True, created_at__date=today)
        elif filter_by == 'week':
            logger.debug('Week filter triggered')
            week = timezone.now().date() - timedelta(days=7)
            shops = Shop.objects.filter(public_access=True, created_at__gte=week)
        elif filter_by:
            logger.debug('Name filter triggered')
            shops = Shop.objects.filter(public_access=True, shop_name=filter_by)
        else:
            logger.debug('Show shops list triggered')
            shops = Shop.objects.filter(public_access=True)

        serializer = ShopSerializer(shops, many=True, fields = ['shop_name', 'public_access', 'shop_creates_name'])
        return Response(serializer.data, status=status.HTTP_200_OK)

class PublicShopDetailView(APIView):
    @extend_schema(
        summary='Public shop details',
        description='Show more details about a specific public shop',
        responses=ShopSerializer,
    )
    def get(self, request, uuid):
        shop = get_object_or_404(Shop, uuid=uuid)
        if not shop.public_access:
            logger.critical('Attempt to access the store without authorization')
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShopSerializer(shop)
        logger.debug('Show shop details triggered')
        return Response(serializer.data, status=status.HTTP_200_OK)

