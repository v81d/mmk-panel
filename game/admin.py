from django.contrib import admin

from .models import Card, Rarity


@admin.register(Rarity)
class RarityAdmin(admin.ModelAdmin):
    list_display = ("name", "desperation_constant")


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("name", "nickname", "rarity")
