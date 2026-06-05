from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import random
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

    @action(detail=False, methods=["get"], url_path="random")
    def random_cards(self, request):
        try:
            count = int(request.query_params.get("count", "1"))
            if count < 1:
                raise ValueError
        except (ValueError, TypeError):
            return Response({"error": "Count must be a positive integer."}, status=400)

        filtered_qs = CardFilterSet(
            request.query_params, queryset=Card.objects.all()
        ).qs
        all_ids = filtered_qs.values_list("id", flat=True)
        random_ids = random.sample(list(all_ids), min(count, len(all_ids)))
        cards = filtered_qs.filter(id__in=random_ids)

        return Response(self.get_serializer(cards, many=True).data)


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
