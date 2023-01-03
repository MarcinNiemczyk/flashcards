import pytest
from django.contrib.auth.models import User
from faker import Faker

from api.models import Box, BoxSettings, Deck

faker = Faker()


@pytest.fixture
def user(db):
    return User.objects.create_user(faker.word())


@pytest.fixture
def deck(db, user):
    return Deck.objects.create(
        name=faker.text(max_nb_chars=50),
        box_amount=faker.random_int(min=1, max=6),
        author=user,
    )


@pytest.fixture
def box_settings(db):
    return BoxSettings.objects.create()


@pytest.fixture
def box(db, deck, box_settings):
    return Box.objects.create(
        number_of=faker.random_int(min=1, max=6),
        deck=deck,
        settings=box_settings,
    )
