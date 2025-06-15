from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name='register'),
    path('my-shops/', views.CreateViewShops.as_view(), name='my-shops'),
    path('public-shops/', views.PublicShopsListView.as_view(), name='public-shops'),
]
