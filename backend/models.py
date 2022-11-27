from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Deck(models.Model):
    name = models.CharField(max_length=50)
    box_amount = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )


class Box(models.Model):
    number_of = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)


class Card(models.Model):
    front = models.CharField(max_length=150)
    back = models.CharField(max_length=150)
    active = models.BooleanField(default=True)
    delay = models.DateTimeField(blank=True, null=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
