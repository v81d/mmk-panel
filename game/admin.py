from django.contrib import admin

from .models import Card, CardMove, CardSprite, Move, Rarity


@admin.register(Rarity)
class RarityAdmin(admin.ModelAdmin):
    list_display = ("name", "desperation_constant")


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "damage")


class CardSpriteInline(admin.TabularInline):
    model = CardSprite
    extra = 1


class CardMoveInline(admin.TabularInline):
    model = CardMove
    extra = 1


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("name", "nickname", "rarity")
    inlines = [CardSpriteInline, CardMoveInline]
