from django_filters import FilterSet, BaseInFilter, NumberFilter

from .models import Card, Move, Rarity


# Filter by list of IDs (i.e., `?ids=0,1,2,3` to retrieve IDs 0, 1, 2, and 3)
class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class CardFilterSet(FilterSet):
    ids = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = Card
        fields = ["name", "nickname", "rarity"]


class MoveFilterSet(FilterSet):
    ids = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = Move
        fields = ["name"]


class RarityFilterSet(FilterSet):
    ids = NumberInFilter(field_name="id", lookup_expr="in")

    class Meta:
        model = Rarity
        fields = "__all__"
