from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModels(TestCase):

    def test_create_user_with_email_succesfful(self):
        """Test that user created with an email successfully"""
        email = "test@akewan.com"
        pwd = "guest"
        user = get_user_model().objects.create_user(
            email=email,
            password=pwd
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(pwd))

    def test_new_user_email_normalized(self):
        """Test the mail for new user is normalized"""
        email = "test@AKEWAN.COM"
        user = get_user_model().objects.create_user(
            email=email,
            password="random_pwd"
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test user without passed email raises ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="random_pwd"
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
                    email="test@akewan.com",
                    password="random_pwd"
                )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
