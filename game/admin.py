from django.contrib import admin

from .models import Card, CardSprite, Rarity


@admin.register(Rarity)
class RarityAdmin(admin.ModelAdmin):
    list_display = ("name", "desperation_constant")


class CardSpriteInline(admin.TabularInline):
    model = CardSprite
    extra = 1


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("name", "nickname", "rarity")
    inlines = [CardSpriteInline]
