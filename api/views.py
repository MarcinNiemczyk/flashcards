from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from api.models import Box, Deck
from api.permissions import IsBoxAuthor, IsDeckAuthor
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
    permission_classes = [IsBoxAuthor]

    def get_queryset(self):
        deck_id = self.kwargs.get("deck_id")
        return Box.objects.filter(deck_id=deck_id).all()
