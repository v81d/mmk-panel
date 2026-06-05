from django_filters import BaseInFilter, CharFilter, FilterSet, NumberFilter

from .models import Card, Move, Rarity


# Filter by list of numbers (e.g.., `?id=0,1,2,3` to retrieve IDs 0, 1, 2, and 3)
class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class CharInFilter(BaseInFilter, CharFilter):
    pass


class BaseIdFilterSet(FilterSet):  # applies to all
    id = NumberInFilter(field_name="id", lookup_expr="in")

    def filter_queryset(self, queryset):
        if self.data is not None and self.data.get("id") == "":
            return queryset.none()
        return super().filter_queryset(queryset)


class CardFilterSet(BaseIdFilterSet):
    name = CharInFilter(field_name="name", lookup_expr="in")
    nickname = CharInFilter(field_name="nickname", lookup_expr="in")
    rarity = NumberInFilter(field_name="rarity__id", lookup_expr="in")

    class Meta:
        model = Card
        fields = ["name", "nickname", "rarity"]


class MoveFilterSet(BaseIdFilterSet):
    name = CharInFilter(field_name="name", lookup_expr="in")
    cost = NumberInFilter(field_name="cost", lookup_expr="in")
    damage = NumberInFilter(field_name="damage", lookup_expr="in")

    class Meta:
        model = Move
        fields = ["name", "cost", "damage"]


class RarityFilterSet(BaseIdFilterSet):
    name = CharInFilter(field_name="name", lookup_expr="in")
    weight = NumberInFilter(field_name="weight", lookup_expr="in")
    desperation_constant = NumberInFilter(
        field_name="desperation_constant", lookup_expr="in"
    )

    class Meta:
        model = Rarity
        fields = ["name", "weight", "desperation_constant"]
