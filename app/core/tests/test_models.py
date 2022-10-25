"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_succesful(self):
        """Test creating a user with an email is succesful"""
        email = 'test@example.com'
        password = 'Testpassword123!;'
        user= get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """Test if email is normalized for new user."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com' ],
            ['Test2@exaMpLe.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['TEST4@example.COM', 'TEST4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'SamplePWD123!;')
            self.assertEqual(user.email, expected)