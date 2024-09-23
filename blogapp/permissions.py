from rest_framework import permissions
from userapp.models import ADMIN, ORDINARY_USER, MANAGER


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(obj.author == request.user or request.user.user_roles == ADMIN or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user.user_roles == ADMIN or request.user.is_superuser)
