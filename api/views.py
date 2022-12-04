from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from api.models import Deck
from api.permissions import IsDeckAuthor
from api.serializers import DeckSerializer


class DeckListView(ListCreateAPIView):
    serializer_class = DeckSerializer

    def get_queryset(self):
        return Deck.objects.filter(author=self.request.user)


class DeckDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
    permission_classes = [IsDeckAuthor]
