from django.db.models import Count
from rest_framework import serializers

from api.models import Box, Deck


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
