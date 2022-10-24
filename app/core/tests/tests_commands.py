"""
Test custom django management commands.
"""

from unittest.mock import patch
from webbrowser import Opera
from django.db import DatabaseError

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for the db to be ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])
    
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for the db when catching OperationalError"""

        ## first two mock calls - [Psycopg2Error] * 2 - raise the psycopg2Error 2 times - when postgres itself isn't up
        ## next 3 mock calls - [OperationalError] * 3 - raise the operational error 3 times - when postgres is up but the db is not ready for requests
        ## finally pass true
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6) 
        patched_check.assert_called_with(databases=['default'])