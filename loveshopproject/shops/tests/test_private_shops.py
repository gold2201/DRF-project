import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.http import Http404
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from shops.models import User, Shop, Product
from shops.services.shop_service import purchase_product, check_shop_object

#Тут просто два unit теста написал
class PurchasesProductTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testPassword')
        self.shop = Shop.objects.create(user=self.user, currency_amount=100)
        self.product = Product.objects.create(shop_id=self.shop.id, product_price=50, product_amount=1, message_after_purchase='Ok')

    def test_purchases_product_success(self):
        success, message = purchase_product(self.shop, self.product)
        self.assertTrue(success)
        self.assertEqual(message, 'Ok')
        self.assertEqual(self.shop.currency_amount, 50)
        self.assertEqual(self.product.product_amount, 0)

    def test_purchases_product_failure(self):
        self.shop.currency_amount = 20
        success, message = purchase_product(self.shop, self.product)
        self.assertFalse(success)
        self.assertEqual(message, 'Not enough currency')
        self.assertEqual(self.shop.currency_amount, 20)

    def test_check_shop_object(self):
        shop_200 = check_shop_object(self.shop.id)
        self.assertEqual(shop_200, self.shop)
        with self.assertRaises(Http404):
            check_shop_object(404)


@pytest.mark.django_db
class TestPrivateShop:
    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='testPass')
        self.client = APIClient()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.publicShop = Shop.objects.create(
            user=self.user,
            public_access=True,
            shop_name='Dima public shop',
            shop_description='Test descr',
            shop_creates_name='Dima',
            currency_name='Тимки',
            currency_amount=12,
        )

        self.privateShop = Shop.objects.create(
            user=self.user,
            public_access=False,
            shop_name='Dima public shop',
            shop_description='Test descr',
            shop_creates_name='Dima',
            access_name='Dima',
            access_password=make_password('password'),
            currency_name='Тимки',
            currency_amount=12,
        )
        self.productPublic = Product.objects.create(shop_id=self.publicShop.id, product_name='test pub prod', product_description='Test descr')
        self.productPrivate = Product.objects.create(shop_id=self.privateShop.id, product_name='test priv prod', product_description='Test descr')

    def test_create_shop(self):
        url = reverse('create-my-shop')
        data = {
                "public_access": "False",
                "shop_name": "Dima public shop",
                "shop_description": "Test descr",
                "shop_creates_name": "Dima",
                "access_name": "Olya",
                "access_password": "fgh123fgh",
                "currency_name": "Тимки",
                "currency_amount": 12,
                "products": [
                    {
                        "product_name": "Banana",
                        "product_description": "Banana yellow",
                        "product_price": 12,
                        "product_amount": 13,
                        "message_after_purchase": "After Banana"
                    }
                ]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['shop_name'] == 'Dima public shop'

    def test_create_shop_incorrect(self):
        url = reverse('create-my-shop')
        data = {
            "public_access": "True",
            "shop_name": "Dima public shop",
            "shop_description": "Test descr",
            "shop_creates_name": "Dima",
            "access_name": "Olya",
            "access_password": "fgh123fgh",
            "currency_name": "Тимки",
            "currency_amount": 12,
            "products": [
                {
                    "product_name": "Banana",
                    "product_description": "Banana yellow",
                    "product_price": 12,
                    "product_amount": 13,
                    "message_after_purchase": "After Banana"
                }
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_my_shops_list(self):
        url = reverse('my-shops')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)
        assert len(response.data) == 2
        assert response.data[0].get('shop_description', None) is None

    def test_work_with_shop_get(self):
        url = reverse('my-shop-detail', kwargs={'pk': self.publicShop.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(url)

        assert response.data['uuid'] == str(self.publicShop.uuid)

    def test_work_with_shop_put_correct(self):
        url = reverse('my-shop-detail', kwargs={'pk': self.publicShop.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {
            "public_access": "True",
            "shop_name": "Dima public shop",
            "shop_description": "Test description",
            "shop_creates_name": "Dima",
            "access_name": "Olya",
            "access_password": "fgh123fgh",
            "currency_name": "Тимки",
            "currency_amount": 12,
            "products": [
                {
                    "id": self.productPublic.id,
                    "product_name": "Test Banana",
                    "product_description": "Banana yellow",
                    "product_price": 12,
                    "product_amount": 13,
                    "message_after_purchase": "After Banana"
                },
                {
                    "product_name": "Banana",
                    "product_description": "Banana yellow",
                    "product_price": 12,
                    "product_amount": 13,
                    "message_after_purchase": "After Banana"
                }
            ]
        }

        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['shop_description'] == 'Test description'
        assert response.data['products'][0]['product_name'] == 'Test Banana'
        assert response.data['products'][1]['product_name'] == 'Banana'

    def test_work_with_shop_put_incorrect(self):
        url = reverse('my-shop-detail', kwargs={'pk': self.publicShop.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {
            "public_access": "True",
            "shop_name": "Dima public shop",
            "shop_description": "Test description",
            "shop_creates_name": "Dima",
            "access_name": "Olya",
            "access_password": "fgh123fgh",
            "currency_name": "Тимки",
            "currency_amount": 12,
            "products": [
                {
                    "id": self.productPrivate.id,
                    "product_name": "Test Banana",
                    "product_description": "Banana yellow",
                    "product_price": 12,
                    "product_amount": 13,
                    "message_after_purchase": "After Banana"
                }
            ]
        }

        response = self.client.put(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_work_with_shop_delete(self):
        url = reverse('my-shop-detail', kwargs={'pk': self.publicShop.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_login_shop(self):
        url = reverse('login-shop')

        correct_data = {
            'access_name':'Dima',
            'access_password':'password'
        }

        incorrect_data = {
            'access_name': 'Dima',
            'access_password': '1234'
        }

        response_200 = self.client.post(url, correct_data, format='json')
        response_400 = self.client.post(url, incorrect_data, format='json')
        assert response_200.status_code == 200
        assert response_200.data['uuid'] == str(self.privateShop.uuid)
        assert response_400.status_code == 400
        assert response_400.data['error'] == 'Invalid password or name'



