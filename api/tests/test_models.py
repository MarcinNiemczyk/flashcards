from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models import Box, Card, Deck


class DeckModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Deck.objects.create(name="foo", box_amount=4)

    def test_name_max_length(self):
        deck = Deck.objects.get(pk=1)
        max_length = deck._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    def test_box_amount_max_value(self):
        try:
            Deck.objects.create(name="foo", box_amount=6)
        except ValidationError:
            self.fail(ValidationError.message)

        with self.assertRaises(ValidationError):
            deck = Deck.objects.create(name="bar", box_amount=7)
            deck.full_clean()

    def test_box_amount_min_value(self):
        try:
            Deck.objects.create(name="foo", box_amount=1)
        except ValidationError:
            self.fail(ValidationError.message)

        with self.assertRaises(ValidationError):
            deck = Deck.objects.create(name="bar", box_amount=0)
            deck.full_clean()


class BoxModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Deck.objects.create(name="foo", box_amount=3)

    def test_new_deck_creates_boxes_properly(self):
        count = Box.objects.count()
        self.assertEqual(count, 3)

    def test_assigned_box_order_is_correct(self):
        box1 = Box.objects.get(pk=1)
        self.assertEqual(box1.number_of, 1)
        box2 = Box.objects.get(pk=2)
        self.assertEqual(box2.number_of, 2)
        box3 = Box.objects.get(pk=3)
        self.assertEqual(box3.number_of, 3)


class CardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        deck = Deck.objects.create(name="foo", box_amount=3)
        Card.objects.create(
            front="foo", back="bar", deck=deck, box=Box.objects.get(pk=1)
        )

    def test_front_max_length(self):
        card = Card.objects.get(pk=1)
        max_length = card._meta.get_field("front").max_length
        self.assertEqual(max_length, 150)

    def test_back_max_length(self):
        card = Card.objects.get(pk=1)
        max_length = card._meta.get_field("back").max_length
        self.assertEqual(max_length, 150)

    def test_default_active(self):
        card = Card.objects.get(pk=1)
        self.assertTrue(card.active)
