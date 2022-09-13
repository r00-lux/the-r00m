from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from rest_framework.test import APIClient
from rest_framework import status


class UserTests(TestCase):
    """Tests for users."""
    def setUp(self):
        self.username = 'plague'
        self.email = 'plague@example.com'
        self.password = 'godsexlovesecret'

    def test_create_user__success(self):
        """Test creating a new user."""
        user = get_user_model().objects.create_user(username=self.username,
                                                    email=self.email,
                                                    password=self.password)

        self.assertEqual(user.username, self.username)
        self.assertTrue(user.check_password(self.password))

    def test_create_user_email_normalized(self):
        """Test email is normalized for new users."""
        emails = [['plague1', 'plague1@EXAMPLE.com', 'plague1@example.com'],
                  ['plague2', 'Plague2@Example.com', 'Plague2@example.com'],
                  ['plague3', 'PLAGUE3@EXAMPLE.COM', 'PLAGUE3@example.com'],
                  ['plague4', 'plague4@example.COM', 'plague4@example.com']]

        for username, email, expected_email in emails:
            user = get_user_model().objects.create_user(
                username, email, self.password)

            self.assertEqual(user.email, expected_email)

    def test_create_user_no_email(self):
        """Test creating user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(self.username, '',
                                                 self.password)

    def test_create_user_no_username(self):
        """Test creating user without a username raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', self.email, self.password)

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            self.username, self.email, self.password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class TestUserAdmin(TestCase):
    """Test user admin."""
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpassword')
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com', username='user', password='userpassword')

    def test_list_users(self):
        """Test admin page users list."""
        url = reverse('admin:users_user_changelist')
        result = self.client.get(url)

        self.assertContains(result, self.user.username)
        self.assertContains(result, self.user.email)

    def test_edit_user_page(self):
        """Test user admin edit page."""
        url = reverse('admin:users_user_change', args=[self.user.id])
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)

    def test_create_user_page(self):
        """Test user admin edit page."""
        url = reverse('admin:users_user_add')
        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)


class PublicUserAPITests(TestCase):
    """Test public user APIs."""
    def setUp(self):
        self.CREATE_USER_URL = reverse('users:create')
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

        result = self.client.post(self.CREATE_USER_URL, payload)

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

        result = self.client.post(self.CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_short_password(self):
        """Test creating user fails when using short password."""
        payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'pw'
        }

        result = self.client.post(self.CREATE_USER_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload.get('email')).exists()
        self.assertFalse(user_exists)
