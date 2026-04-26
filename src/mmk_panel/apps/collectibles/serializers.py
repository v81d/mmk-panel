from rest_framework.serializers import ModelSerializer

from .models import Card, Move, Rarity


# Serializers define the API representation
class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


class MoveSerializer(ModelSerializer):
    class Meta:
        model = Move
        fields = "__all__"


class RaritySerializer(ModelSerializer):
    class Meta:
        model = Rarity
        fields = "__all__"
