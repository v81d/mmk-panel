from rest_framework.serializers import ModelSerializer

from .models import Card, CardMove, Move, Rarity


# Serializers define the API representation
class RaritySerializer(ModelSerializer):
    class Meta:
        model = Rarity
        fields = "__all__"


class MoveSerializer(ModelSerializer):
    class Meta:
        model = Move
        fields = "__all__"


class CardMoveSerializer(ModelSerializer):
    move = MoveSerializer(read_only=True)

    class Meta:
        model = CardMove
        fields = "__all__"


class CardSerializer(ModelSerializer):
    moves = CardMoveSerializer(source="cardmove_set", many=True, read_only=True)
    rarity = RaritySerializer(read_only=True)

    class Meta:
        model = Card
        fields = "__all__"
