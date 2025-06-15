from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from shops.models import Shop
from shops.serializers import ShopSerializer

class PublicShopsListView(APIView):

    def get(self, request):
        filter_by = request.query_params.get('filter_by', None)

        if filter_by == 'today':
            today = datetime.now().date()
            shops = Shop.objects.filter(public_access=True, created_at__date=today)
        elif filter_by == 'week':
            week = datetime.now().date() - timedelta(days=7)
            shops = Shop.objects.filter(public_access=True, created_at__gte=week)
        elif filter_by:
            shops = Shop.objects.filter(public_access=True, shop_name=filter_by)
        else:
            shops = Shop.objects.filter(public_access=True)

        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)