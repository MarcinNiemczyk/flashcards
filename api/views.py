from rest_framework import viewsets

from api.models import Deck
from api.serializers import DeckSerializer


class DeckViewSet(viewsets.ModelViewSet):
    serializer_class = DeckSerializer

    def get_queryset(self):
        return Deck.objects.filter(author=self.request.user)
