from django.urls import reverse

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


def move_card_to_next_box(card_id):
    card = Card.objects.get(pk=card_id)
    if card.deck.box_amount > card.box.number_of:
        new_box = Box.objects.get(
            deck=card.deck, number_of=card.box.number_of + 1
        )
        card.box = new_box
        card.save()


def move_card_to_first_box(card_id):
    card = Card.objects.get(pk=card_id)
    new_box = Box.objects.get(deck=card.deck, number_of=1)
    card.box = new_box
    card.save()
