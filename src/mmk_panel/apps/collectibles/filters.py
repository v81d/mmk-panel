from django_filters import FilterSet, BaseInFilter, NumberFilter

from .models import Card, Move, Rarity


# Filter by list of IDs (e.g.., `?ids=0,1,2,3` to retrieve IDs 0, 1, 2, and 3)
class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class BaseIdFilterSet(FilterSet):
    ids = NumberInFilter(field_name="id", lookup_expr="in")

    def filter_queryset(self, queryset):
        if not (self.data or {}).get("ids"):
            return queryset.none()

        return super().filter_queryset(queryset)


class CardFilterSet(BaseIdFilterSet):
    class Meta:
        model = Card
        fields = ["name", "nickname", "rarity"]


class MoveFilterSet(BaseIdFilterSet):
    class Meta:
        model = Move
        fields = ["name"]


class RarityFilterSet(BaseIdFilterSet):
    class Meta:
        model = Rarity
        fields = "__all__"
