from django.urls import path, include
from rest_framework.routers import DefaultRouter

from item import views


router = DefaultRouter()
router.register("tags", views.TagViewset)

app_name = "item"

urlpatterns = [
    path("", include(router.urls))
]
