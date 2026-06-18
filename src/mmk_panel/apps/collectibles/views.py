import random

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

        weighted = request.query_params.get("weighted", "false").lower() == "true"

        filtered_qs = CardFilterSet(
            request.query_params, queryset=Card.objects.select_related("rarity")
        ).qs

        all_cards = list(filtered_qs)
        if not all_cards:
            return Response([])

        count = min(count, len(all_cards))

        if weighted:
            weights = [1.0 / card.rarity.weight for card in all_cards]
            remaining_cards = list(all_cards)
            remaining_weights = list(weights)
            chosen = []
            for _ in range(count):
                [pick] = random.choices(remaining_cards, weights=remaining_weights, k=1)
                chosen.append(pick)
                idx = remaining_cards.index(pick)
                remaining_cards.pop(idx)
                remaining_weights.pop(idx)
        else:
            chosen = random.sample(all_cards, count)

        return Response(self.get_serializer(chosen, many=True).data)


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
