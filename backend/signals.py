from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.models import Box, Deck


@receiver(post_save, sender=Deck)
def generate_boxes(sender, instance, created, **kwargs):
    for i in range(1, instance.box_amount + 1):
        Box.objects.create(number_of=i, deck=instance)
