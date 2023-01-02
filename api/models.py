from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Settings(models.Model):
    delay_correct = models.PositiveSmallIntegerField(
        default=3, help_text="Delay card after correct answer in days"
    )
    delay_wrong = models.PositiveSmallIntegerField(
        default=3, help_text="Delay card after wrong answer in days"
    )
    reverse = models.BooleanField(
        default=False, help_text="Reverse card to question by rear side"
    )
    random_order = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Settings"


class Deck(models.Model):
    name = models.CharField(max_length=50)
    box_amount = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Box(models.Model):
    class Meta:
        verbose_name_plural = "boxes"

    number_of = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    settings = models.ForeignKey(Settings, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.number_of)}/{str(self.deck.box_amount)} ({self.deck.name})"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.settings = Settings.objects.create()
        super().save(*args, **kwargs)


class Card(models.Model):
    front = models.CharField(max_length=150)
    back = models.CharField(max_length=150)
    active = models.BooleanField(default=True)
    delay = models.DateTimeField(blank=True, null=True)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
