from django.test import TestCase
from django.contrib.auth import get_user_model


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
