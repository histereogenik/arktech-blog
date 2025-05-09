from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperUserOrReadOnly(BasePermission):
    """
    Allow public to read (GET), but only superusers can modify.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Public read
        return request.user and request.user.is_superuser
