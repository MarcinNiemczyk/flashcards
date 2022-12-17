from django.urls import reverse


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
