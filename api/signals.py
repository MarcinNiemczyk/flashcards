from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Box, Card, Deck


@receiver(post_save, sender=Deck)
def generate_boxes(sender, instance, created, **kwargs):
    deck = instance
    if created:
        for i in range(1, deck.box_amount + 1):
            Box.objects.create(number_of=i, deck=deck)
    else:
        current_boxes = Box.objects.filter(deck=deck).count()
        new_box_amount = deck.box_amount

        # Adding boxes to existing deck
        if new_box_amount > current_boxes:
            for i in range(current_boxes, new_box_amount):
                Box.objects.create(number_of=i + 1, deck=deck)

        # Reducing boxes in existing deck
        elif new_box_amount < current_boxes:
            new_last_box = Box.objects.get(number_of=new_box_amount, deck=deck)
            for i in range(current_boxes, new_box_amount, -1):
                box = Box.objects.get(number_of=i, deck=deck)
                Card.objects.filter(box=box).update(box=new_last_box)
                box.delete()
