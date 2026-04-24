from django.db import models


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
    spritesheet = models.ImageField(upload_to="cards/spritesheets/")
    description = models.TextField()
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
