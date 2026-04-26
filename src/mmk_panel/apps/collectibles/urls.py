from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CardViewSet, MoveViewSet, RarityViewSet

router = DefaultRouter()
router.register("cards", CardViewSet)
router.register("moves", MoveViewSet)
router.register("rarities", RarityViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
