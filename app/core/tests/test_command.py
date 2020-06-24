from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class TestCommand(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db till db is available"""
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            gi.return_value = True
            call_command("wait_for_db")
            gi.assert_called_once()

    @patch("time.sleep", return_value=True)
    def test_wait_for_db(self, sleep):
        """Test waiting for db."""
        with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
            side_effects = [OperationalError] * 5 + [True]
            gi.side_effect = side_effects
            call_command("wait_for_db")
            self.assertEqual(gi.call_count, len(side_effects))
