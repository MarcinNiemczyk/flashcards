from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from api.models import Box, Card


def get_deck_detail_absolute_url(request, deck_id):
    url = reverse("deck-detail", kwargs={"pk": deck_id})
    return request.build_absolute_uri(url)


def get_deck_boxes_absolute_url(request, deck_id):
    url = reverse("box-list") + "?deck=" + str(deck_id)
    return request.build_absolute_uri(url)


def get_deck_cards_absolute_url(request, deck_id):
    url = reverse("card-list") + "?deck=" + str(deck_id)
    return request.build_absolute_uri(url)


def get_box_cards_absolute_url(request, box_id):
    url = reverse("card-list") + "?box=" + str(box_id)
    return request.build_absolute_uri(url)


def get_box_detail_absolute_url(request, box_id):
    url = reverse("box-detail", kwargs={"pk": box_id})
    return request.build_absolute_uri(url)


def get_card_detail_absolute_url(request, card_id):
    url = reverse("card-detail", kwargs={"pk": card_id})
    return request.build_absolute_uri(url)


def add_boxes_in_deck(deck):
    for i in range(1, deck.box_amount + 1):
        Box.objects.create(number_of=i, deck=deck)


def reduce_boxes_in_deck(deck):
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


def move_card_to_next_box(card_id):
    card = Card.objects.get(pk=card_id)
    if card.deck.box_amount > card.box.number_of:
        new_box = Box.objects.get(
            deck=card.deck, number_of=card.box.number_of + 1
        )
        __move_card(card, new_box)


def move_card_to_first_box(card_id):
    card = Card.objects.get(pk=card_id)
    new_box = Box.objects.get(deck=card.deck, number_of=1)
    __move_card(card, new_box)


def __move_card(card, box):
    card.box = box
    __delay_card(card)
    card.save()


def __delay_card(card):
    """Hide card to the start of nth day"""

    card.active = False
    current_time = timezone.now()
    card.delay = (
        current_time
        + timedelta(3)
        - timedelta(
            days=0,
            hours=current_time.hour,
            minutes=current_time.minute,
            seconds=current_time.second,
            microseconds=current_time.microsecond,
        )
    )
