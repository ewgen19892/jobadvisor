"""Users permissions."""
from django.views import View

from rest_framework import permissions
from rest_framework.request import Request

from jobadvisor.users.models import User


class UserPermission(permissions.BasePermission):
    """User permissions."""

    def has_object_permission(self, request: Request, view: View,
                              obj: User) -> bool:
        """
        Check user permission.

        :param request: Request object
        :param view: View
        :param obj: User object
        :return: Bool
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj
