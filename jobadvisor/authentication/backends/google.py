"""Facebook auth backend."""
from django.utils.translation import ugettext_lazy as _

from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.exceptions import APIException

from jobadvisor.authentication.backends.base import BaseBackend


class GoogleException(APIException):
    """Google exception."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Google exception")


class PermissionException(GoogleException):
    """Google permission exception."""

    default_detail = _("No required permissions")


class GoogleBackend(BaseBackend):
    """Google backend."""

    @staticmethod
    def _normalize_user_data(user_data: dict) -> dict:
        """
        Normalize user data.

        :param user_data: User data from google
        :return: normalized user data.
        """
        try:
            data = {
                "first_name": user_data["given_name"],
                "last_name": user_data["family_name"],
                "email": user_data["email"],
                "photo_url": user_data["picture"],
            }
        except KeyError:
            raise PermissionException
        return data

    def get_user_data(self, token: str) -> dict:
        """
        Get user data from Google.

        :param token: access token
        :return: User data.
        """
        try:
            user_data = id_token.verify_oauth2_token(token, requests.Request())
        except Exception as error:
            raise GoogleException(detail=str(error))
        return self._normalize_user_data(user_data)
