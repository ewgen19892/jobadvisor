"""Companies exceptions."""
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException


class MaxFavoriteReview(APIException):
    """Limit of favorite review."""

    status_code = status.HTTP_409_CONFLICT
    default_code = "conflict"
    default_detail = _("Limit of favorite reviews exceeded")


class MaxFavoriteInterview(APIException):
    """Limit of favorite interviews."""

    status_code = status.HTTP_409_CONFLICT
    default_code = "conflict"
    default_detail = _("Limit of favorite interviews exceeded")
