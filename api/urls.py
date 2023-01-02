from django.urls import path

from api.views import (
    AnswerView,
    BoxDetailView,
    BoxListView,
    CardDetailView,
    CardListView,
    DeckDetailView,
    DeckListView,
    SettingsView,
)

urlpatterns = [
    path("decks/", DeckListView.as_view(), name="deck-list"),
    path("decks/<int:pk>", DeckDetailView.as_view(), name="deck-detail"),
    path("boxes/", BoxListView.as_view(), name="box-list"),
    path("boxes/<int:pk>", BoxDetailView.as_view(), name="box-detail"),
    path(
        "boxes/<int:pk>/settings", SettingsView.as_view(), name="box-settings"
    ),
    path("cards/", CardListView.as_view(), name="card-list"),
    path("cards/<int:pk>", CardDetailView.as_view(), name="card-detail"),
    path("cards/<int:pk>/answer", AnswerView.as_view(), name="answer"),
]
