from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag
from item.serializers import TagSerializer


TAG_URL = reverse("item:tag-list")


class PublicTagApiTest(TestCase):
    """Test cases for puvlic Tag API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test case that login is reuqired for tag API"""
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):
    """Test cases for the authorized user Tag API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="akewan@akewan.com",
            password="guest",
            name="Test"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name="Shirt")
        Tag.objects.create(user=self.user, name="Underwear")

        res = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_to_user(self):
        """Test to retrieve tags only for authenticated user"""
        other_user = get_user_model().objects.create_user(
            email="akemaki@akewan.com",
            password="guest",
        )
        Tag.objects.create(user=other_user, name="Socks")
        tag = Tag.objects.create(user=self.user, name="Shirt")

        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {
            "name": "TestTag"
        }
        self.client.post(TAG_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload["name"]
        ).exists()

        self.assertTrue(exists)

    def test_creeate_tag_invlid(self):
        """Test creating a new tag with invalid payload"""
        payload = {"mame": ""}
        res = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
