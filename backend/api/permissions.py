from rest_framework.permissions import BasePermission

class IsFRUser(BasePermission):
    """
    Allows access only to users from France.
    """
    def has_permission(self, request, *args, **kwargs):
        return request.user.is_authenticated and request.user.is_fr

class IsDZUser(BasePermission):
    """
    Allows access only to users from Algeria.
    """
    def has_permission(self, request, *args, **kwargs):
        return request.user.is_authenticated and request.user.is_dz
