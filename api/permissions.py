from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from api.models import Deck


class IsDeckAuthor(BasePermission):
    message = "Only deck author can access his deck"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsBoxAuthor(BasePermission):
    message = "Only deck author can access his boxes"

    def has_permission(self, request, view):
        deck_id = request.parser_context.get("kwargs").get("deck_id")
        deck = get_object_or_404(Deck, pk=deck_id)
        return request.user == deck.author
