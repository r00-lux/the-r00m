import django
from django.test import TestCase


class DBTests(TestCase):
    """Tests that the site database is functional."""
    def test_db_connection(self):
        result = django.db.connection.ensure_connection()

        self.assertEqual(result, None)
