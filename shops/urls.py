from django.urls import path
from .views import userViews, publicShopViews, authentificatedShopViews

urlpatterns = [
    path('register/', userViews.UserRegistration.as_view(), name='register'),
    path('my-shops/', authentificatedShopViews.MyShopsListView.as_view(), name='my-shops'),
    path('create-my-shop/', authentificatedShopViews.CreateViewShops.as_view(), name='create-my-shop'),
    path('my-shop-detail/', authentificatedShopViews.WorkWithShopView.as_view(), name='my-shop-detail'),
    path('public-shops/', publicShopViews.PublicShopsListView.as_view(), name='public-shops'),
]
