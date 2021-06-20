"""Companies exceptions."""
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException, PermissionDenied


class NotWorker(PermissionDenied):
    """User is not an employee."""

    default_detail = _("You are not an employee of the company")


class NoActiveSubscription(PermissionDenied):
    """The company has no active subscription."""

    default_detail = _("The company does not have the active subscription")


class NoRequiredSubscription(PermissionDenied):
    """The company does not have the required subscription."""

    default_detail = _("The company does not have the required subscription")


class MaxTopVacancies(APIException):
    """Limit of top vacancies."""

    status_code = status.HTTP_409_CONFLICT
    default_code = "conflict"
    default_detail = _("Limit of top vacancy exceeded")
