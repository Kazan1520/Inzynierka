# isadminorreadonly permisison

from rest_framework import permissions
from rest_framework.permissions import IsAdminUser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user



