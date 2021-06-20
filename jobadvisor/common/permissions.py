"""JobAdvisor permissions."""
from typing import Any

from django.views import View

from rest_framework import permissions
from rest_framework.request import Request


class OwnerPermission(permissions.BasePermission):
    """Owner permissions."""

    def has_object_permission(self, request: Request, view: View,
                              obj: Any) -> bool:
        """
        Check user permission.

        :param request: Request object
        :param view: View
        :param obj: User object
        :return: Bool
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner
