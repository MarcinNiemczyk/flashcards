from django.urls import path

from api.views import BoxListView, DeckDetailView, DeckListView

urlpatterns = [
    path("decks/", DeckListView.as_view(), name="deck-list"),
    path("decks/<pk>", DeckDetailView.as_view(), name="deck-detail"),
    path("decks/<int:deck_id>/boxes/", BoxListView.as_view(), name="box-list"),
]
