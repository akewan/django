from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API is public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Testcase to create user with valid payload."""
        payload = {
            "email": "akewan@akewan.com",
            "password": "guest",
            "name": "Archer"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Create a user that alreay exist faiils"""
        payload = {
            "email": "akewan@akewan.com",
            "password": "guest",
            "name": "Archer"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def password_too_short(self):
        """Password must be more then 5 chars"""
        payload = {
            "email": "akewan@akewan.com",
            "password": "ab",
            "name": "Archer"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        )
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            "email": "akewan@akewan.com",
            "password": "guest",
            "name": "Archer"
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_create_token_inmalid_creds(self):
        """Test that token is not created if invalid creds are given"""
        create_user(email="akewam@akewan.com", password="guest")
        payload = {
            "email": "akewan@akewan.com",
            "password": "wrong"
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_create_token_no_user(self):
        """test that token not created if user not exists"""
        payload = {
            "email": "akewan@akewan.com",
            "password": "guest",
            "name": "Archer"
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_missing_password_field(self):
        """Email and pass are required"""
        res = self.client.post(TOKEN_URL, {'email': "some", "password": ""})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)
