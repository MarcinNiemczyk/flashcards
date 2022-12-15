from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from api.models import Box, Card, Deck


class DeckViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("foo", "foo@foo.com", "foo")
        User.objects.create_user("bar", "bar@bar.com", "bar")
        Deck.objects.create(
            name="foodeck", box_amount=1, author=User.objects.get(pk=1)
        )
        Deck.objects.create(
            name="bardeck", box_amount=1, author=User.objects.get(pk=2)
        )

    def setUp(self):
        self.client.force_login(User.objects.get(pk=1))

    def test_list_view_exists_at_desired_location(self):
        response = self.client.get(reverse("deck-list"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/decks/")
        self.assertEqual(response.status_code, 200)

    def test_detail_view_exists_at_desired_location(self):
        response = self.client.get(reverse("deck-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/decks/1")
        self.assertEqual(response.status_code, 200)

    def test_list_view_returns_only_own_decks(self):
        response = self.client.get(reverse("deck-list"))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], 1)

    def test_detail_view_permission_set_to_author_only(self):
        response = self.client.get(reverse("deck-detail", kwargs={"pk": 2}))
        self.assertEqual(response.status_code, 403)

    def test_output_contains_expected_fields(self):
        response = self.client.get(reverse("deck-detail", kwargs={"pk": 1}))
        expected_fields = ["id", "name", "box_amount", "total_cards"]
        self.assertCountEqual(response.data, expected_fields)

    def test_output_returns_total_cards_count(self):
        response = self.client.get(reverse("deck-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data.get("total_cards"), 0)

        Card.objects.create(
            front="foo",
            back="bar",
            box=Box.objects.get(pk=1),
            deck=Deck.objects.get(pk=1),
        )
        response = self.client.get(reverse("deck-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data.get("total_cards"), 1)

    def test_total_cards_count_only_desired_deck(self):
        Deck.objects.create(
            name="foodeck", box_amount=1, author=User.objects.get(pk=1)
        )
        Card.objects.create(
            front="foo",
            back="bar",
            box=Box.objects.get(pk=1),
            deck=Deck.objects.get(pk=1),
        )
        Card.objects.create(
            front="foo",
            back="bar",
            box=Box.objects.get(pk=3),
            deck=Deck.objects.get(pk=1),
        )
        response = self.client.get(reverse("deck-detail", kwargs={"pk": 1}))
        self.assertEqual(response.data.get("total_cards"), 1)
        response = self.client.get(reverse("deck-detail", kwargs={"pk": 3}))
        self.assertEqual(response.data.get("total_cards"), 1)

    def test_total_cards_count_all_boxes_from_deck(self):
        deck = Deck.objects.create(
            name="foodeck", box_amount=3, author=User.objects.get(pk=1)
        )
        for i in range(deck.box_amount):
            box = Box.objects.get(deck=deck, number_of=i + 1)
            Card.objects.create(
                front="foo", back="bar", box=box, deck=Deck.objects.get(pk=1)
            )
        response = self.client.get(reverse("deck-detail", kwargs={"pk": 3}))
        self.assertEqual(response.data.get("total_cards"), 3)

    def test_input_contains_expected_fields(self):
        response = self.client.post(reverse("deck-list"))
        expected_fields = ["name", "box_amount"]
        self.assertEqual(response.status_code, 400)
        self.assertCountEqual(response.data, expected_fields)

    def test_deck_creation_sets_request_author_automatically(self):
        response = self.client.post(
            reverse("deck-list"),
            {"name": "newdeck", "box_amount": 1},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        author = User.objects.get(pk=1)
        new_deck = Deck.objects.get(name="newdeck")
        self.assertEqual(new_deck.author, author)


class BoxViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user("foo", "foo@foo.com", "foo")
        User.objects.create_user("bar", "bar@bar.com", "bar")
        Deck.objects.create(
            name="foodeck", box_amount=1, author=User.objects.get(pk=1)
        )
        Deck.objects.create(
            name="bardeck", box_amount=1, author=User.objects.get(pk=2)
        )

    def setUp(self):
        self.client.force_login(User.objects.get(pk=1))

    def test_box_view_exists_at_desired_location(self):
        response = self.client.get(reverse("box-list"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/boxes/")
        self.assertEqual(response.status_code, 200)

    def test_only_list_method_is_allowed(self):
        response = self.client.options(reverse("box-list"))
        allowed_methods = response.headers.get("Allow").split(", ")
        expected_methods = ["GET", "HEAD", "OPTIONS"]
        self.assertCountEqual(allowed_methods, expected_methods)

    def test_user_can_access_only_own_deck_boxes(self):
        response = self.client.get("/api/boxes/?deck=2")
        self.assertEqual(response.data, [])

    def test_output_contains_expected_fields(self):
        response = self.client.get("/api/boxes/?deck=1")
        expected_fields = ["id", "number_of", "total_cards"]
        self.assertCountEqual(response.data[0], expected_fields)

    def test_total_cards_count_cards_for_specific_box(self):
        response = self.client.get("/api/boxes/?deck=1")
        self.assertEqual(response.data[0]["total_cards"], 0)

        Card.objects.create(
            front="foo",
            back="bar",
            box=Box.objects.get(pk=1),
            deck=Deck.objects.get(pk=1),
        )
        response = self.client.get("/api/boxes/?deck=1")
        self.assertEqual(response.data[0]["total_cards"], 1)
