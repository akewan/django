from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Feature
from item.serializers import FeatureSerializer


FEATURE_URL = reverse("item:feature-list")


class PublicFeatureApiTest(TestCase):
    """Test cases for puvlic Feature API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test case that login is reuqired for tag API"""
        res = self.client.get(FEATURE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFeatureApiTest(TestCase):
    """Test cases for the authorized user Feature API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="akewan@akewan.com",
            password="guest",
            name="Test"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_feature_list(self):
        """Test retrieving a list of features"""
        Feature.objects.create(user=self.user, name="color")
        Feature.objects.create(user=self.user, name="size")

        res = self.client.get(FEATURE_URL)

        features = Feature.objects.all().order_by("-name")
        serializer = FeatureSerializer(features, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_features_limited_to_user(self):
        """Test that features only for authenticated user returned"""
        other_user = get_user_model().objects.create_user(
            email="akemaki@akewan.com",
            password="guest",
        )
        Feature.objects.create(user=other_user, name="color")
        feature = Feature.objects.create(user=self.user, name="size")

        res = self.client.get(FEATURE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], feature.name)

    def test_create_feature_successful(self):
        """Test creating a new feature"""
        payload = {
            "name": "TestFeature"
        }
        self.client.post(FEATURE_URL, payload)

        exists = Feature.objects.filter(
            user=self.user,
            name=payload["name"]
        ).exists()

        self.assertTrue(exists)

    def test_creeate_feature_invlid(self):
        """Test creating a new feature with invalid payload"""
        payload = {"mame": ""}
        res = self.client.post(FEATURE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
