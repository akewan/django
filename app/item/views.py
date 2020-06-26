from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Feature
from item.serializers import TagSerializer, FeatureSerializer


class TagViewset(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage Tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class FeatureViewset(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    """Manage features in the databse"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user"""
        return self.queryset.filter(user=self.request.user)
