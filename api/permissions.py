from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_superuser
        )


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user == obj.user
        )