from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class HealthAPITests(TestCase):
    """Test health api."""
    def setUp(self):
        self.client = APIClient()

    def test_health_api_reachable(self):
        """Test health api is reachable."""
        result = self.client.get('/api/health/')

        self.assertEqual(result.status_code, status.HTTP_200_OK)
