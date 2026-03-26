from rest_framework import permissions

class IsVerifiedAlumnus(permissions.BasePermission):
    """
    Allows access only to users whose 'isverified' status is True.
    """
    def has_permission(self, request, view):
        # Check if user is logged in AND if their profile is verified
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'isverified', False)
        )