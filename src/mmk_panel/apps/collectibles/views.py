from rest_framework import viewsets

from .filters import CardFilterSet, MoveFilterSet, RarityFilterSet
from .models import Card, Move, Rarity
from .serializers import CardSerializer, MoveSerializer, RaritySerializer


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows cards to be viewed.
    """

    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filterset_class = CardFilterSet


class MoveViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows moves to be viewed.
    """

    queryset = Move.objects.all()
    serializer_class = MoveSerializer
    filterset_class = MoveFilterSet


class RarityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows rarities to be viewed.
    """

    queryset = Rarity.objects.all()
    serializer_class = RaritySerializer
    filterset_class = RarityFilterSet
