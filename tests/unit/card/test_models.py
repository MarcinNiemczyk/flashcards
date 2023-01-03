import pytest


@pytest.mark.django_db
def test_front_max_length(card):
    front_max_length = card._meta.get_field("front").max_length
    assert front_max_length == 150


@pytest.mark.django_db
def test_back_max_length(card):
    back_max_length = card._meta.get_field("back").max_length
    assert back_max_length == 150


@pytest.mark.django_db
def test_active_default_value(card):
    active_default = card._meta.get_field("active").default
    assert active_default is True


@pytest.mark.django_db
def test_delay_field_can_be_blank(card):
    delay_blank = card._meta.get_field("delay").blank
    assert delay_blank is True


@pytest.mark.django_db
def test_delay_field_is_nullable(card):
    delay_nullable = card._meta.get_field("delay").null
    assert delay_nullable is True
