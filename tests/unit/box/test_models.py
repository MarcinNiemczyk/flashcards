import pytest
from django.core.exceptions import ValidationError

from api.models import Box


@pytest.mark.django_db
def test_verbose_name_plural(box):
    verbose_name_plural = box._meta.verbose_name_plural
    assert verbose_name_plural == "boxes"


@pytest.mark.django_db
def test_number_of_min_value_edge_case(deck, box_settings):
    try:
        box = Box.objects.create(number_of=1, deck=deck, settings=box_settings)
        box.clean_fields()
    except ValidationError:
        pytest.fail()


@pytest.mark.django_db
def test_number_of_below_min_value_raises_error(deck, box_settings):
    with pytest.raises(ValidationError):
        box = Box.objects.create(number_of=0, deck=deck, settings=box_settings)
        box.clean_fields()


@pytest.mark.django_db
def test_number_of_max_value_edge_case(deck, box_settings):
    try:
        box = Box.objects.create(number_of=6, deck=deck, settings=box_settings)
        box.clean_fields()
    except ValidationError:
        pytest.fail()


@pytest.mark.django_db
def test_number_of_above_max_value_raises_error(deck, box_settings):
    with pytest.raises(ValidationError):
        box = Box.objects.create(number_of=7, deck=deck, settings=box_settings)
        box.clean_fields()


@pytest.mark.django_db
def test_object_str_name_is_desired_value(box):
    expected_value = (
        f"{str(box.number_of)}/{str(box.deck.box_amount)} ({box.deck.name})"
    )
    assert str(box) == expected_value
