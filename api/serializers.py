from django.db.models import Count
from rest_framework import serializers

from api.models import Box, Card, Deck, Settings
from api.utils import (
    get_box_cards_absolute_url,
    get_box_detail_absolute_url,
    get_box_settings_absolute_url,
    get_card_detail_absolute_url,
    get_deck_boxes_absolute_url,
    get_deck_cards_absolute_url,
    get_deck_detail_absolute_url,
)


class SettingsSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Settings
        fields = [
            "delay_correct",
            "delay_wrong",
            "reverse",
            "random_order",
            "links",
        ]

    def get_links(self, obj):
        request = self.context["request"]
        box = Box.objects.get(settings=obj)
        return {
            "box": get_box_detail_absolute_url(request, box.id),
        }


class DeckSerializer(serializers.ModelSerializer):
    total_cards = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Deck
        fields = [
            "name",
            "box_amount",
            "total_cards",
            "links",
        ]

    def get_total_cards(self, obj):
        return Box.objects.filter(deck=obj).aggregate(Count("card"))[
            "card__count"
        ]

    def get_links(self, obj):
        request = self.context["request"]
        return {
            "self": get_deck_detail_absolute_url(request, obj.id),
            "boxes": get_deck_boxes_absolute_url(request, obj.id),
            "cards": get_deck_cards_absolute_url(request, obj.id),
        }

    def create(self, validated_data):
        author = self.context.get("request").user
        deck = Deck(author=author, **validated_data)
        deck.save()
        return deck


class BoxSerializer(serializers.ModelSerializer):
    total_cards = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Box
        fields = ["number_of", "total_cards", "links"]

    def get_total_cards(self, obj):
        return obj.card_set.count()

    def get_links(self, obj):
        request = self.context["request"]
        return {
            "self": get_box_detail_absolute_url(request, obj.id),
            "settings": get_box_settings_absolute_url(request, obj.id),
            "deck": get_deck_detail_absolute_url(request, obj.deck.id),
            "cards": get_box_cards_absolute_url(request, obj.id),
        }


class UserDecksForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context["request"].user
        return Deck.objects.filter(author=user)


class CardListSerializer(serializers.ModelSerializer):
    deck = UserDecksForeignKey(write_only=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ["front", "back", "active", "delay", "deck", "links"]
        read_only_fields = ["active", "delay"]

    def get_links(self, obj):
        request = self.context["request"]
        return {
            "self": get_card_detail_absolute_url(request, obj.id),
            "box": get_box_detail_absolute_url(request, obj.box.id),
            "deck": get_deck_detail_absolute_url(request, obj.deck.id),
        }

    def create(self, validated_data):
        box = Box.objects.get(deck=validated_data.get("deck"), number_of=1)
        card = Card(box=box, **validated_data)
        card.save()
        return card


class DeckBoxesForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        if self.parent.instance is not None:
            return Box.objects.filter(deck=self.parent.instance.deck)


class CardDetailSerializer(serializers.ModelSerializer):
    box = DeckBoxesForeignKey(write_only=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ["front", "back", "active", "delay", "box", "links"]
        read_only_fields = ["active", "delay"]

    def get_links(self, obj):
        request = self.context["request"]
        return {
            "self": get_card_detail_absolute_url(request, obj.id),
            "box": get_box_detail_absolute_url(request, obj.box.id),
            "deck": get_deck_detail_absolute_url(request, obj.deck.id),
        }


class AnswerSerializer(serializers.Serializer):
    answer = serializers.BooleanField(write_only=True)
