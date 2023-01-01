from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Deck
from api.utils import add_boxes_in_deck, reduce_boxes_in_deck


@receiver(post_save, sender=Deck)
def generate_boxes(sender, instance, created, **kwargs):
    if created:
        add_boxes_in_deck(deck=instance)
    else:
        reduce_boxes_in_deck(deck=instance)
