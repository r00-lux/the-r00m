from django.test import TestCase
from django.contrib.auth import get_user_model


class ProfileTests(TestCase):
    """Tests for users."""
    def test_create_user__success(self):
        """Test creating a new profile."""
        username = 'plague'
        email = 'plague@example.com'
        password = 'godsexlovesecret'
        user = get_user_model().objects.create_user(username=username,
                                                    email=email,
                                                    password=password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_user_email_normalized(self):
        """Test email is normalized for new users."""
        emails = [['plague1', 'plague1@EXAMPLE.com', 'plague1@example.com'],
                  ['plague2', 'Plague2@Example.com', 'Plague2@example.com'],
                  ['plague3', 'PLAGUE3@EXAMPLE.COM', 'PLAGUE3@example.com'],
                  ['plague4', 'plague4@example.COM', 'plague4@example.com']]

        for username, email, expected_email in emails:
            user = get_user_model().objects.create_user(
                username, email, 'godsexlovesecret')

            self.assertEqual(user.email, expected_email)
