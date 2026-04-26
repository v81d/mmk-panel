import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models


# Pre-upload hook/procedure to randomize the filename by generating a UUID
def card_sprite_upload_to(_, filename):
    ext = filename.split(".")[-1]
    return f"cards/sprites/{uuid.uuid4()}.{ext}"


def move_sprite_upload_to(_, filename):
    ext = filename.split(".")[-1]
    return f"moves/sprites/{uuid.uuid4()}.{ext}"


class Rarity(models.Model):
    class Meta:
        verbose_name_plural = "Rarities"

    name = models.CharField(max_length=50)
    desperation_constant = models.PositiveIntegerField()

    def __str__(self):
        return self.name


# Insanely long model even though most of the fields are optional :(
class Move(models.Model):
    name = models.CharField(max_length=50)
    sprite = models.ImageField(upload_to=move_sprite_upload_to)
    cost = models.PositiveIntegerField(null=True, blank=True)
    damage = models.PositiveIntegerField(null=True, blank=True)

    # Self properties
    self_defense_multiplier = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    self_attack_multiplier = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    self_move_energy_multiplier = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    self_move_energy_gain_multiplier = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    self_desperation_multiplier = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    self_defense_scalar_boost = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    self_attack_scalar_boost = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    self_move_energy_scalar_boost = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    self_move_energy_gain_scalar_boost = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    self_poison = ArrayField(models.FloatField(), size=2, null=True, blank=True)
    self_prevent_move = models.PositiveIntegerField(null=True, blank=True)

    # Enemy properties
    enemy_defense_multiplier = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    enemy_attack_multiplier = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    enemy_move_energy_multiplier = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    enemy_move_energy_gain_multiplier = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    enemy_desperation_multiplier = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    enemy_defense_scalar_boost = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    enemy_attack_scalar_boost = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    enemy_move_energy_scalar_boost = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    enemy_move_energy_gain_scalar_boost = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    enemy_desperation_scalar_boost = ArrayField(
        models.FloatField(), size=2, null=True, blank=True
    )
    enemy_poison = ArrayField(models.FloatField(), size=2, null=True, blank=True)
    enemy_prevent_move = models.PositiveIntegerField(null=True, blank=True)  # stun

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
    desperation = models.FloatField()

    def __str__(self):
        return self.name


# This class is not exactly a model on its own, but rather an inline model that should be placed as a Card field
class CardSprite(models.Model):
    card = models.ForeignKey("Card", on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    image = models.ImageField(upload_to=card_sprite_upload_to)


class CardMove(models.Model):
    card = models.ForeignKey("Card", on_delete=models.CASCADE)
    move = models.ForeignKey("Move", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
