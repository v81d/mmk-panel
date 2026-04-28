import uuid
from io import BytesIO

from django.contrib.postgres.fields import ArrayField
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image


# Pre-upload hook/procedure to randomize the filename by generating a UUID
def card_sprite_upload_to(_, filename):
    ext = filename.split(".")[-1]
    return f"collectibles/cards/sprites/{uuid.uuid4()}.{ext}"


def card_audio_upload_to(_, filename):
    ext = filename.split(".")[-1]
    return f"collectibles/cards/audio/{uuid.uuid4()}.{ext}"


def move_sprite_upload_to(_, filename):
    ext = filename.split(".")[-1]
    return f"collectibles/moves/sprites/{uuid.uuid4()}.{ext}"


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
    self_custom_dialogue = models.TextField(null=True, blank=True)

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
    enemy_custom_dialogue = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=100)
    description = models.TextField()
    default_sprite = models.ImageField(
        upload_to=card_sprite_upload_to
    )  # required sprite field
    audio = models.FileField(upload_to=card_audio_upload_to, null=True, blank=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    health = models.PositiveIntegerField()
    defense = models.PositiveIntegerField()
    base_move_energy = models.PositiveIntegerField()
    base_move_energy_gain = models.PositiveIntegerField()
    desperation = models.FloatField()

    def save(self, *args, **kwargs):
        if self.default_sprite:
            image = Image.open(self.default_sprite)
            image_format = image.format

            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            image_io = BytesIO()
            image.save(
                image_io, image_format, optimize=True, quality=70
            )  # compress to 70% quality
            image_content = ContentFile(
                image_io.getvalue(), name=self.default_sprite.name
            )

            self.default_sprite = image_content

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# This class is not exactly a model on its own, but rather an inline model that should be placed as a Card field
class CardMove(models.Model):
    card = models.ForeignKey("Card", on_delete=models.CASCADE)
    move = models.ForeignKey("Move", on_delete=models.CASCADE)
    sprite = models.ImageField(
        upload_to=move_sprite_upload_to, null=True, blank=True
    )  # optional; moves that do not have a unique sprite will use the default sprite

    def save(self, *args, **kwargs):
        if self.sprite:
            image = Image.open(self.sprite)
            image_format = image.format

            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            image_io = BytesIO()
            image.save(image_io, image_format, optimize=True, quality=70)
            image_content = ContentFile(image_io.getvalue(), name=self.sprite.name)

            self.sprite = image_content

        super().save(*args, **kwargs)
