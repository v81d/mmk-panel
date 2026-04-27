from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from .forms import MoveAdminForm
from .models import Card, CardMove, Move, Rarity


@admin.register(Rarity)
class RarityAdmin(ModelAdmin):
    list_display = ("id", "name", "desperation_constant")
    ordering = ["id"]


@admin.register(Move)
class MoveAdmin(ModelAdmin):
    form = MoveAdminForm
    list_display = ("id", "name", "cost", "damage")
    ordering = ["id"]

    fieldsets = (
        (
            "General Metadata",
            {
                "fields": (
                    "name",
                    "cost",
                    "damage",
                )
            },
        ),
        (
            "Self Effects",
            {
                "fields": (
                    "self_defense_multiplier",
                    "self_attack_multiplier",
                    "self_move_energy_multiplier",
                    "self_move_energy_gain_multiplier",
                    "self_desperation_multiplier",
                    "self_defense_scalar_boost",
                    "self_attack_scalar_boost",
                    "self_move_energy_scalar_boost",
                    "self_move_energy_gain_scalar_boost",
                    "self_poison",
                    "self_prevent_move",
                ),
            },
        ),
        (
            "Enemy Effects",
            {
                "fields": (
                    "enemy_defense_multiplier",
                    "enemy_attack_multiplier",
                    "enemy_move_energy_multiplier",
                    "enemy_move_energy_gain_multiplier",
                    "enemy_desperation_multiplier",
                    "enemy_defense_scalar_boost",
                    "enemy_attack_scalar_boost",
                    "enemy_move_energy_scalar_boost",
                    "enemy_move_energy_gain_scalar_boost",
                    "enemy_desperation_scalar_boost",
                    "enemy_poison",
                    "enemy_prevent_move",
                ),
            },
        ),
    )


class CardMoveInline(TabularInline):
    model = CardMove
    extra = 1


@admin.register(Card)
class CardAdmin(ModelAdmin):
    inlines = [CardMoveInline]
    list_display = ("id", "name", "nickname", "rarity")
    ordering = ["id"]

    fieldsets = (
        (
            "General Metadata",
            {"fields": ("name", "nickname", "description", "default_sprite", "rarity")},
        ),
        (
            "Attributes",
            {
                "fields": (
                    "health",
                    "defense",
                    "base_move_energy",
                    "base_move_energy_gain",
                    "desperation",
                )
            },
        ),
    )
