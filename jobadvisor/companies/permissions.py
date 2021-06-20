"""Companies permissions."""
from django.utils.translation import gettext_lazy as _
from django.views import View

from rest_framework import permissions
from rest_framework.request import Request

from jobadvisor.companies.models import Company, Subscription, Vacancy


class CompanyPermission(permissions.BasePermission):
    """Company permissions."""

    SAFE_METHODS = ("GET", "HEAD", "OPTIONS", "DELETE")
    message = _("The company must have a first subscription")

    def has_object_permission(self, request: Request, view: View,
                              obj: Company) -> bool:
        """
        Check company permission.

        :param request:
        :param view:
        :param obj:
        :return:
        """
        if request.method in self.SAFE_METHODS:
            return True
        return obj.has_perm(Subscription.FIRST, request.user)


class CompanyFollowPermission(permissions.BasePermission):
    """Company permissions."""

    SAFE_METHODS = ("GET", "HEAD", "OPTIONS", "DELETE")
    message = _("The company must have a second subscription")

    def has_object_permission(self, request: Request, view: View,
                              obj: Company) -> bool:
        """
        Check company's permission to get followers.

        :param request:
        :param view:
        :param obj:
        :return:
        """
        if request.method == "GET":
            return obj.has_perm(Subscription.SECOND, request.user)
        return True


class VacancyPermission(permissions.BasePermission):
    """Vacancy permissions."""

    message = _("The company must have a second subscription")

    def has_object_permission(self, request: Request, view: View,
                              obj: Vacancy) -> bool:
        """
        Check vacancy permission.

        :param request: Request object
        :param view: View
        :param obj: User object
        :return: Bool
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.company.has_perm(Subscription.SECOND, request.user)


class VacancyRespondedPermission(permissions.BasePermission):
    """Vacancy favorite list permissions."""

    message = _("The company must have a second subscription")

    def has_object_permission(self, request: Request, view: View,
                              obj: Vacancy) -> bool:
        """
        Check vacancy permission.

        :param request: Request object
        :param view: View
        :param obj: User object
        :return: Bool
        """
        if request.method == "GET":
            return obj.company.has_perm(Subscription.SECOND, request.user)
        return True


class VacancyResponsePermission(permissions.BasePermission):
    """Vacancy create permissions."""

    message = _("User must have a resume")

    def has_object_permission(self, request: Request, view: View,
                              obj: Vacancy) -> bool:
        """
        Check vacancy permission.

        :param request: Request object
        :param view: View
        :param obj: User object
        :return: Bool
        """
        if request.method == "POST":
            return hasattr(request.user, "resumes")
        return True


class VacancyTopPermission(permissions.BasePermission):
    """Vacancy top permissions."""

    message = _("The company must have a third subscription")
    authenticated_users_only = True

    def has_object_permission(self, request: Request, view: View,
                              obj: Vacancy) -> bool:
        """
        Check vacancy permission.

        :param request: Request object
        :param view: View
        :param obj: User object
        :return: Bool
        """
        return obj.company.has_perm(Subscription.THIRD, request.user)
