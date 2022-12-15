from django.db.models import Count
from rest_framework import serializers

from api.models import Box, Card, Deck


class DeckSerializer(serializers.ModelSerializer):
    total_cards = serializers.SerializerMethodField()

    class Meta:
        model = Deck
        fields = ["id", "name", "box_amount", "total_cards"]

    def get_total_cards(self, obj):
        return Box.objects.filter(deck=obj).aggregate(Count("card"))[
            "card__count"
        ]

    def create(self, validated_data):
        author = self.context.get("request").user
        deck = Deck(author=author, **validated_data)
        deck.save()
        return deck


class BoxSerializer(serializers.ModelSerializer):
    total_cards = serializers.SerializerMethodField()

    class Meta:
        model = Box
        fields = ["id", "number_of", "total_cards"]

    def get_total_cards(self, obj):
        return obj.card_set.count()


class UserDecksForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context["request"].user
        return Deck.objects.filter(author=user)


class CardListSerializer(serializers.ModelSerializer):
    deck = UserDecksForeignKey()

    class Meta:
        model = Card
        fields = ["id", "front", "back", "active", "delay", "box", "deck"]
        read_only_fields = ["active", "delay", "box", "deck"]
        extra_kwargs = {
            "deck": {"write_only": True},
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
    box = DeckBoxesForeignKey()

    class Meta:
        model = Card
        fields = ["id", "front", "back", "active", "delay", "box", "deck"]
        read_only_fields = ["active", "delay", "box", "deck"]
        extra_kwargs = {
            "box": {"write_only": True},
        }
