from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from api.models import Box


class IsDeckAuthor(BasePermission):
    message = "Only deck author can access his deck"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsBoxAuthor(BasePermission):
    message = "Only deck author can access his boxes"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.deck.author


class IsSettingsBoxAuthor(BasePermission):
    message = "Only deck author can access his boxes"

    def has_permission(self, request, view):
        pk = view.kwargs.get("pk")
        box = get_object_or_404(Box, pk=pk)
        return request.user == box.deck.author


class IsCardAuthor(BasePermission):
    message = "Only deck author can modify his cards"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.deck.author
