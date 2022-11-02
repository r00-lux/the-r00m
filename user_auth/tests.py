from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

TOKEN_URL = reverse('user_auth:token')


def create_user(**params):
    """Create a test user."""
    return get_user_model().objects.create_user(**params)


class AuthTests(TestCase):
    """Test auth app."""

    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_data = {
            'name': 'foo',
            'username': 'foo',
            'email': 'foo@bar.com',
            'password': 'foo-bar-baz'
        }
        # Generate a test user.
        create_user(**user_data)

        # Payload for the API. Use username and password to authenticate.
        payload = {
            'username': user_data.get('username'),
            'password': user_data.get('password')
        }
        # POST to the API.
        res = self.client.post(TOKEN_URL, payload)

        # Confirm we got a token back.
        self.assertIn('token', res.data)
        # Confirm we got a 200 status code.
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(username='test_user',
                    email='test@example.com',
                    password='goodpass')

        payload = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'badpass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns error."""
        payload = {'username': 'tester', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
