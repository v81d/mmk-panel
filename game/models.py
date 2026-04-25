import uuid

from django.db import models


# Pre-upload hook/procedure to randomize the filename by generating a UUID
def card_sprite_upload_to(instance, filename):
    ext = filename.split(".")[-1]
    new_name = f"{uuid.uuid4()}.{ext}"
    return f"cards/sprites/{new_name}"


class Rarity(models.Model):
    class Meta:
        verbose_name_plural = "Rarities"

    name = models.CharField(max_length=50)
    desperation_constant = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=100)
    description = models.TextField()
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    health = models.PositiveIntegerField()
    defense = models.PositiveIntegerField()
    base_move_energy = models.PositiveIntegerField()
    base_move_energy_gain = models.PositiveIntegerField()
    desperation = models.PositiveIntegerField()

    def __str__(self):
        return self.name


# This class is not exactly a model on its own, but rather an inline model that should be placed as a Card field
class CardSprite(models.Model):
    card = models.ForeignKey("Card", on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to=card_sprite_upload_to,
    )
