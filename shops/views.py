from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils.representation import serializer_repr
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

from shops.models import User, Shop, Product
from shops.serializers import UserSerializer, ShopSerializer, ProductSerializer

class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateViewShops(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        shops = Shop.objects.filter(user=user)
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response(serializer.data)





#lass ItemListDetailView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

#   queryset = Shop.objects.all()
#   serializer_class = ShopSerializer

#   def get(self, request, *args, **kwargs):
#       return self.list(request, *args, **kwargs)

#   def post(self, request, *args, **kwargs):
#       return self.create(request, *args, **kwargs)

#lass DetailItemView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#   queryset = Shop.objects.all()
#   serializer_class = ShopSerializer

#   def get(self, request, *args, **kwargs):
#       return self.retrieve(request, *args, **kwargs)

#   def put(self, request, *args, **kwargs):
#       return self.update(request, *args, **kwargs)

#   def delete(self, request, *args, **kwargs):
#       return self.destroy(request, *args, **kwargs)
