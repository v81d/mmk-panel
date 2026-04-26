from django_filters import FilterSet

from .models import Card, Move, Rarity


class CardFilterSet(FilterSet):
    class Meta:
        model = Card
        fields = ["name", "nickname", "rarity"]


class MoveFilterSet(FilterSet):
    class Meta:
        model = Move
        fields = ["name"]


class RarityFilterSet(FilterSet):
    class Meta:
        model = Rarity
        fields = "__all__"
