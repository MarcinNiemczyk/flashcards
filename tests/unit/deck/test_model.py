import pytest
from django.core.exceptions import ValidationError

from api.models import Deck
from tests.conftest import faker


@pytest.mark.django_db
def test_name_max_length(deck):
    max_length = deck._meta.get_field("name").max_length
    assert max_length == 50


@pytest.mark.django_db
def test_box_amount_min_value_edge_case(user):
    try:
        deck = Deck.objects.create(
            name=faker.text(max_nb_chars=50), box_amount=1, author=user
        )
        deck.full_clean()
    except ValidationError:
        pytest.fail()


@pytest.mark.django_db
def test_box_amount_below_min_value_raises_error(user):
    with pytest.raises(ValidationError):
        deck = Deck.objects.create(
            name=faker.text(max_nb_chars=50), box_amount=0, author=user
        )
        deck.full_clean()


@pytest.mark.django_db
def test_box_amount_max_value_edge_case(user):
    try:
        deck = Deck.objects.create(
            name=faker.text(max_nb_chars=50), box_amount=6, author=user
        )
        deck.full_clean()
    except ValidationError:
        pytest.fail()


@pytest.mark.django_db
def test_box_amount_above_max_value_raises_error(user):
    with pytest.raises(ValidationError):
        deck = Deck.objects.create(
            name=faker.text(max_nb_chars=50), box_amount=7, author=user
        )
        deck.full_clean()


@pytest.mark.django_db
def test_object_str_name_is_deck_name(deck):
    assert str(deck) == deck.name
