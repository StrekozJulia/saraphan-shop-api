from rest_framework import permissions


class CartPermission(permissions.BasePermission):
    """Проверка прав для действий с корзиной."""
    message = ('Действия с чужой корзиной невозможны.')

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user
