from django.urls import path
from .views import userViews, publicShopViews, authentificatedShopViews

urlpatterns = [
    path('register/', userViews.UserRegistration.as_view(), name='register'),
    path('my-shops/', authentificatedShopViews.MyShopsListView.as_view(), name='my-shops'),
    path('create-my-shop/', authentificatedShopViews.CreateViewShops.as_view(), name='create-my-shop'),
    path('my-shop-detail/<int:pk>/', authentificatedShopViews.WorkWithShopView.as_view(), name='my-shop-detail'),
    path('login-shop/', authentificatedShopViews.AccessedPrivateShopView.as_view(), name='login-shop'),
    path('authorized-shop/<uuid:uuid>/', authentificatedShopViews.WorkWithAccessedShopView.as_view(), name='authorized-shop'),
    path('product-purchase/<uuid:uuid>/<int:pk>/', authentificatedShopViews.WorkWithAccessedShopView.as_view(), name='authorized-shop'),
    path('public-shops/', publicShopViews.PublicShopsListView.as_view(), name='public-shops'),
    path('public-shop-detail/<int:pk>/', publicShopViews.PublicShopDetailView.as_view(), name='public-shop-detail'),
]
