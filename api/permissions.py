from rest_framework.permissions import BasePermission


class IsDeckAuthor(BasePermission):
    message = "Only deck author can access his deck"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
