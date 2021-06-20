"""Reviews permissions."""
from typing import Any

from django.views import View

from rest_framework import permissions
from rest_framework.request import Request

from jobadvisor.companies.models import Subscription
from jobadvisor.reviews.models import QA


class QAPermission(permissions.BasePermission):
    """QA permissions."""

    def has_object_permission(self, request: Request, view: View,
                              obj: QA) -> bool:
        """
        Check QA permission.

        :param request: Request object
        :param view: View
        :param obj: User object
        :return: Bool
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.interview.owner


class CommentPermission(permissions.BasePermission):
    """Comment permissions."""

    def has_object_permission(self, request: Request, view: View,
                              obj: Any) -> bool:
        """
        Check QA permission.

        :param request: Request object
        :param view: View
        :param obj: User object
        :return: Bool
        """
        return obj.company.has_perm(Subscription.FIRST, request.user,
                                    raise_exception=True)


class CompanyFavoritePermission(permissions.BasePermission):
    """Company favorite permissions."""

    def has_object_permission(self, request: Request, view: View,
                              obj: Any) -> bool:
        """
        Check QA permission.

        :param request: Request object
        :param view: View
        :param obj: User object
        :return: Bool
        """
        return obj.company.has_perm(Subscription.SECOND, request.user,
                                    raise_exception=True)
