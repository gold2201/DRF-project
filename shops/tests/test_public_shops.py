import uuid
from datetime import timedelta
from unittest import mock

from django.utils import timezone

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shops.models import Shop

class PublicShopsTestCase(APITestCase):
    def setUp(self):
        self.now = timezone.now()

        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.publicShop1 = Shop.objects.create(
            user=self.user,
            uuid=uuid.uuid4(),
            public_access=True,
            shop_name='Dima public shop',
            created_at=self.now - timedelta(days=5),
            shop_description='Test descr',
            shop_creates_name='Dima',
            currency_name='Тимки',
            currency_amount=12,
        )

        self.publicShop2 = Shop.objects.create(
            user=self.user,
            uuid=uuid.uuid4(),
            public_access=True,
            shop_name='Dima public shop 2',
            created_at=self.now,
            shop_description='Test descr',
            shop_creates_name='Dima',
            currency_name='Тимки',
            currency_amount=12,
        )

        self.privateShop = Shop.objects.create(
            user=self.user,
            uuid=uuid.uuid4(),
            public_access=False,
            shop_name='Dima public shop',
            created_at=self.now,
            shop_description='Test descr',
            shop_creates_name='Dima',
            access_name='Dima',
            access_password='password',
            currency_name='Тимки',
            currency_amount=12,
        )

    def test_public_shop_detail(self):
        urlpublic = reverse('public-shop-detail', kwargs={'uuid': self.publicShop1.uuid})
        urlprivate = reverse('public-shop-detail', kwargs={'uuid': self.privateShop.uuid})

        response_for_public = self.client.get(urlpublic)
        response_for_private = self.client.get(urlprivate)

        self.assertEqual(response_for_public.status_code, status.HTTP_200_OK)
        self.assertEqual(response_for_private.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_shop_filter(self):
        url = reverse('public-shops')

        with mock.patch('django.utils.timezone.now', return_value=self.now):
            response_for_today_filter = self.client.get(url, {'filter_by': 'today'})
            response_for_week_filter = self.client.get(url, {'filter_by': 'week'})
            response_for_name_filter = self.client.get(url, {'filter_by': self.publicShop1.shop_name})

        correct_week_shops = [self.publicShop1.shop_name, self.publicShop2.shop_name]
        response_week_shops = [response_for_week_filter.data[0]['shop_name'], response_for_week_filter.data[1]['shop_name']]

        self.assertEqual(response_for_today_filter.status_code, status.HTTP_200_OK)
        self.assertEqual(response_for_week_filter.status_code, status.HTTP_200_OK)
        self.assertEqual(response_for_name_filter.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response_for_today_filter.data), 1)
        self.assertEqual(len(response_for_week_filter.data), 2)
        self.assertEqual(len(response_for_name_filter.data), 1)

        self.assertEqual(response_for_today_filter.data[0]['shop_name'], self.publicShop2.shop_name)
        self.assertEqual(response_week_shops, correct_week_shops)
        self.assertEqual(response_for_name_filter.data[0]['shop_name'], self.publicShop1.shop_name)