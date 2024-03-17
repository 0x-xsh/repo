from rest_framework.permissions import BasePermission

class IsFRUser(BasePermission):
    """
    Allows access to only FR User.
    """
    def has_permission(self, request, *args, **kwargs):
        return request.user.is_authenticated and request.user.is_fr

class IsDZUser(BasePermission):
    """
    Allows access to only DZ Users.
    """
    def has_permission(self, request, *args, **kwargs):
        return request.user.is_authenticated and request.user.is_dz
