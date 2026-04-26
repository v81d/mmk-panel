from rest_framework import permissions, viewsets

from .models import Card, Move, Rarity
from .serializers import CardSerializer, MoveSerializer, RaritySerializer


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to be viewed.
    """

    queryset = Card.objects.all().order_by("name")
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MoveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows moves to be viewed.
    """

    queryset = Move.objects.all().order_by("name")
    serializer_class = MoveSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RarityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rarities to be viewed.
    """

    queryset = Rarity.objects.all().order_by("name")
    serializer_class = RaritySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
