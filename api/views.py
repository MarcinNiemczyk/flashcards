from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from api.models import Box, Deck
from api.permissions import IsDeckAuthor
from api.serializers import BoxSerializer, DeckSerializer


class DeckListView(ListCreateAPIView):
    serializer_class = DeckSerializer

    def get_queryset(self):
        return Deck.objects.filter(author=self.request.user)


class DeckDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
    permission_classes = [IsDeckAuthor]


class BoxListView(ListAPIView):
    serializer_class = BoxSerializer

    def get_queryset(self):
        queryset = Box.objects.filter(deck__author=self.request.user).all()
        deck_id = self.request.query_params.get("deck")
        if deck_id is not None:
            queryset = queryset.filter(deck__id=deck_id)
        return queryset
