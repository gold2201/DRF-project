from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


User = get_user_model()

class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'strongpassword123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], data['username'])

    def test_password_verification(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 1234
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

