from django.urls import path

from api.views import (
    BoxListView,
    CardDetailView,
    CardListView,
    DeckDetailView,
    DeckListView,
)

urlpatterns = [
    path("decks/", DeckListView.as_view(), name="deck-list"),
    path("decks/<int:pk>", DeckDetailView.as_view(), name="deck-detail"),
    path("boxes/", BoxListView.as_view(), name="box-list"),
    path("cards/", CardListView.as_view(), name="card-list"),
    path("cards/<int:pk>", CardDetailView.as_view(), name="card-detail"),
]
