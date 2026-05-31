import uuid
from io import BytesIO

from colorfield.fields import ColorField
from django.contrib.postgres.fields import ArrayField
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
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

    weight = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    plate_color = ColorField()
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
        if self.pk:
            try:
                old = Card.objects.get(pk=self.pk)
                if old.default_sprite and old.default_sprite != self.default_sprite:
                    old.default_sprite.delete(save=False)  # type: ignore[union-attr]
                if old.audio and old.audio != self.audio:
                    old.audio.delete(save=False)  # type: ignore[union-attr]
            except Card.DoesNotExist:
                pass

        if self.default_sprite and isinstance(self.default_sprite.file, UploadedFile):
            from rembg import remove

            assert self.default_sprite.name, "default_sprite has no filename in Card"
            input_bytes = self.default_sprite.file.read()
            output_bytes = remove(input_bytes)
            image = Image.open(BytesIO(output_bytes))  # type: ignore[arg-type]
            image_io = BytesIO()
            image.save(image_io, "PNG", optimize=True)
            self.default_sprite = ContentFile(
                image_io.getvalue(),
                name=self.default_sprite.name.rsplit(".", 1)[0] + ".png",
            )

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
        if self.pk and self.sprite:
            try:
                old = CardMove.objects.get(pk=self.pk)
                if old.sprite and old.sprite != self.sprite:
                    old.sprite.delete(save=False)  # type: ignore[union-attr]
            except CardMove.DoesNotExist:
                pass

        if self.sprite and isinstance(self.sprite.file, UploadedFile):
            from rembg import remove

            assert self.sprite.name, "sprite has no filename in CardMove"
            input_bytes = self.sprite.file.read()
            output_bytes = remove(input_bytes)
            image = Image.open(BytesIO(output_bytes))  # type: ignore[arg-type]
            image_io = BytesIO()
            image.save(image_io, "PNG", optimize=True)
            self.sprite = ContentFile(
                image_io.getvalue(),
                name=self.sprite.name.rsplit(".", 1)[0] + ".png",
            )

        super().save(*args, **kwargs)


@receiver(post_delete, sender=Card)
def delete_card_files(sender, instance, **kwargs):
    if instance.default_sprite:
        instance.default_sprite.delete(save=False)
    if instance.audio:
        instance.audio.delete(save=False)


@receiver(post_delete, sender=CardMove)
def delete_card_move_files(sender, instance, **kwargs):
    if instance.sprite:
        instance.sprite.delete(save=False)
