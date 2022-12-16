from rest_framework.permissions import BasePermission


class IsDeckAuthor(BasePermission):
    message = "Only deck author can access his deck"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsBoxAuthor(BasePermission):
    message = "Only deck author can access his boxes"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.deck.author


class IsCardAuthor(BasePermission):
    message = "Only deck author can modify his cards"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.deck.author
