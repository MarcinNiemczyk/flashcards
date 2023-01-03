import pytest


@pytest.mark.django_db
def test_verbose_name_plural(box_settings):
    verbose_name_plural = box_settings._meta.verbose_name_plural
    assert verbose_name_plural == "Box Settings"


@pytest.mark.django_db
def test_delay_correct_default_value(box_settings):
    delay_correct_default = box_settings._meta.get_field(
        "delay_correct"
    ).default
    assert delay_correct_default == 3


@pytest.mark.django_db
def test_delay_correct_help_text(box_settings):
    delay_correct_help_text = box_settings._meta.get_field(
        "delay_correct"
    ).help_text
    assert delay_correct_help_text == "Delay card after correct answer in days"


@pytest.mark.django_db
def test_delay_wrong_default_value(box_settings):
    delay_wrong_default = box_settings._meta.get_field("delay_wrong").default
    assert delay_wrong_default == 3


@pytest.mark.django_db
def test_delay_wrong_help_text(box_settings):
    delay_wrong_help_text = box_settings._meta.get_field(
        "delay_wrong"
    ).help_text
    assert delay_wrong_help_text == "Delay card after wrong answer in days"


@pytest.mark.django_db
def test_reverse_field_default_value(box_settings):
    reverse_default = box_settings._meta.get_field("reverse").default
    assert reverse_default is False


@pytest.mark.django_db
def test_reverse_field_help_text(box_settings):
    reverse_field_help_text = box_settings._meta.get_field("reverse").help_text
    assert reverse_field_help_text == "Reverse card to question by rear side"


@pytest.mark.django_db
def test_random_order_default_value(box_settings):
    random_order_default = box_settings._meta.get_field("random_order").default
    assert random_order_default is False
