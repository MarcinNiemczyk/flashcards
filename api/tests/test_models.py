from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from api.models import Box, Card, Deck


class DeckModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user("foo", "foo@bar.com", "baz")
        Deck.objects.create(name="foo", box_amount=4, author=user)

    def test_name_max_length(self):
        deck = Deck.objects.get(pk=1)
        max_length = deck._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    def test_box_amount_max_value(self):
        user = User.objects.get(pk=1)
        Deck.objects.create(name="foo", box_amount=6, author=user)

        with self.assertRaises(ValidationError):
            deck = Deck.objects.create(name="bar", box_amount=7, author=user)
            deck.full_clean()

    def test_box_amount_min_value(self):
        user = User.objects.get(pk=1)
        Deck.objects.create(name="foo", box_amount=1, author=user)

        with self.assertRaises(ValidationError):
            deck = Deck.objects.create(name="bar", box_amount=0, author=user)
            deck.full_clean()

    def test_object_name_is_deck_name(self):
        deck = Deck.objects.get(pk=1)
        self.assertEqual(deck.name, str(deck))


class BoxModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user("foo", "foo@bar.com", "baz")
        Deck.objects.create(name="foo", box_amount=3, author=user)

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

    def test_update_deck_box_amount_to_higher_value_adds_boxes(self):
        deck = Deck.objects.get(pk=1)
        expected_box_amount = deck.box_amount + 1
        deck.box_amount = expected_box_amount
        deck.save()
        self.assertEqual(Box.objects.count(), expected_box_amount)

    def test_update_deck_box_amount_to_lower_value_reduces_box_objects(self):
        deck = Deck.objects.get(pk=1)
        expected_box_amount = deck.box_amount - 1
        deck.box_amount = expected_box_amount
        deck.save()
        self.assertEqual(Box.objects.count(), expected_box_amount)

    def test_update_deck_to_equal_value_does_not_change_anything(self):
        deck = Deck.objects.get(pk=1)
        expected_box_amount = deck.box_amount
        deck.box_amount = expected_box_amount
        deck.save()
        self.assertEqual(Box.objects.count(), expected_box_amount)

    def test_update_deck_box_amount_to_lower_value_moves_cards_to_last_deck(
        self,
    ):
        deck = Deck.objects.get(pk=1)
        box_amount = deck.box_amount
        cards_per_deck = 5
        for number_of in range(1, box_amount + 1):
            box = Box.objects.get(number_of=number_of, deck=deck)
            for i in range(cards_per_deck):
                Card.objects.create(
                    front="foo", back="bar", box=box, deck=deck
                )
        expected_total_cards = box_amount * cards_per_deck
        self.assertEqual(Card.objects.count(), expected_total_cards)

        reduce_number = 2
        deck.box_amount = box_amount - reduce_number
        deck.save()
        new_last_box = Box.objects.get(number_of=deck.box_amount, deck=deck)
        self.assertEqual(Card.objects.count(), expected_total_cards)
        expected_cards_in_last_deck = (
            reduce_number * cards_per_deck + cards_per_deck
        )
        self.assertEqual(
            new_last_box.card_set.count(), expected_cards_in_last_deck
        )

    def test_object_name_is_number_of_and_deck_name(self):
        box = Box.objects.get(pk=1)
        number_of = str(box.number_of)
        box_count = str(Box.objects.count())
        deck_name = box.deck.name
        expected_object_name = f"{number_of}/{box_count} ({deck_name})"
        self.assertEqual(expected_object_name, str(box))


class CardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user("foo", "foo@bar.com", "baz")
        deck = Deck.objects.create(name="foo", box_amount=1, author=user)
        Card.objects.create(
            front="bar", back="baz", box=Box.objects.get(pk=1), deck=deck
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
