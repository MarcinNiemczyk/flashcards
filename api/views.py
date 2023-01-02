from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from api.models import Box, Card, Deck, Settings
from api.permissions import (
    IsBoxAuthor,
    IsCardAuthor,
    IsDeckAuthor,
    IsSettingsBoxAuthor,
)
from api.serializers import (
    AnswerSerializer,
    BoxSerializer,
    CardDetailSerializer,
    CardListSerializer,
    DeckSerializer,
    SettingsSerializer,
)
from api.utils import move_card_to_first_box, move_card_to_next_box


class SettingsView(RetrieveUpdateAPIView):
    serializer_class = SettingsSerializer
    permission_classes = [IsSettingsBoxAuthor]

    def get_object(self):
        pk = self.kwargs.get("pk")
        box = Box.objects.select_related("settings").get(pk=pk)
        return box.settings


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
        queryset = Box.objects.filter(deck__author=self.request.user)
        deck_id = self.request.query_params.get("deck")
        if deck_id is not None:
            queryset = queryset.filter(deck__id=deck_id)
        return queryset


class BoxDetailView(RetrieveAPIView):
    serializer_class = BoxSerializer
    permission_classes = [IsBoxAuthor]
    queryset = Box.objects.all()


class CardListView(ListCreateAPIView):
    serializer_class = CardListSerializer

    def get_queryset(self):
        queryset = Card.objects.filter(deck__author=self.request.user)
        deck_id = self.request.query_params.get("deck")
        box_id = self.request.query_params.get("box")
        if deck_id is not None:
            queryset = queryset.filter(deck__id=deck_id)
        if box_id is not None:
            queryset = queryset.filter(box__id=box_id)
        return queryset


class CardDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardDetailSerializer
    permission_classes = [IsCardAuthor]


class AnswerView(CreateAPIView):
    serializer_class = AnswerSerializer

    def create(self, request, pk, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        answer = serializer.validated_data.get("answer")
        if answer is True:
            move_card_to_next_box(card_id=pk)
            return Response(
                {"message": "Card has been moved to the next Box!"}
            )
        else:
            move_card_to_first_box(card_id=pk)
            return Response(
                {"message": "Card has been moved to the first Box :("}
            )
