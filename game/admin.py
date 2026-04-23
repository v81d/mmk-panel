from django.contrib import admin

from .models import Card, Rarity

admin.site.register(Rarity)
admin.site.register(Card)
