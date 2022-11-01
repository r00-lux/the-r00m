from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')


def create_user(**params):
    """Create a test user."""
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test public user APIs."""

    def setUp(self):
        self.client = APIClient()

    def create_user(self, **params):
        """Helper to create a new user."""
        return get_user_model().objects.create_user(**params)

    def test_create_user(self):
        """Test creating a user."""
        payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'name': 'Chuck Tester'
        }

        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload.get('email'))
        self.assertTrue(user.check_password(payload.get('password')))
        self.assertNotIn('password', result.data)

    def test_create_user_email_exists(self):
        """Test creating user with existing email fails."""
        payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password'
        }
        self.create_user(**payload)

        result = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_short_password(self):
        """Test creating user fails when using short password."""
        payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'pw'
        }

        result = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload.get('email')).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'username': 'tester',
            'email': 'test@example.com',
            'password': 'test-password-123'
        }
        create_user(**user_details)

        payload = {
            'username': user_details.get('username'),
            'password': user_details.get('password')
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
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
