from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'PUT', 'DELETE', 'PATCH']:
            return obj.user == request.user
        else:
            return False
