from django.urls import path

from api.views import DeckDetailView, DeckListView

urlpatterns = [
    path("decks/", DeckListView.as_view()),
    path("decks/<pk>", DeckDetailView.as_view()),
]
