from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        """Return if user can edit profile."""
        if request.method in permissions.SAFE_METHODS:
            return True

        return object.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    def has_object_permission(self, request, view, object):
        """Return if user can edit their own status."""
        if request.method in permissions.SAFE_METHODS:
            return True

        return object.user_profile.id == request.user.id
