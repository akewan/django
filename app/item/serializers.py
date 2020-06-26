from rest_framework import serializers

from core.models import Tag, Feature


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag objects"""

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class FeatureSerializer(serializers.ModelSerializer):
    """Serializer for Feature objects"""

    class Meta:
        model = Feature
        fields = ("id", "name")
        read_only_fields = ("id",)
