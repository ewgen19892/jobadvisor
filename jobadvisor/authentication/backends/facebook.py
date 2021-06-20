"""Facebook auth backend."""
from django.utils.translation import ugettext_lazy as _

import facebook
from rest_framework import status
from rest_framework.exceptions import APIException

from jobadvisor.authentication.backends.base import BaseBackend


class FacebookException(APIException):
    """Facebook exception."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Facebook exception")


class PermissionException(FacebookException):
    """Facebook permission exception."""

    default_detail = _("No required permissions")


class FacebookBackend(BaseBackend):
    """Facebook backend."""

    permissions: tuple = (
        "first_name",
        "last_name",
        "email",
        "picture.type(large)",
    )

    @staticmethod
    def _normalize_user_data(user_data: dict) -> dict:
        """
        Normalize user data.

        :param user_data: User data from facebook
        :return: normalized user data.
        """
        try:
            data = {
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "email": user_data["email"],
                "photo_url": user_data["picture"]["data"]["url"],
            }
            return data
        except KeyError:
            raise PermissionException

    def get_user_data(self, token: str) -> dict:
        """
        Get user data.

        :param token: Access token for GraphAPI
        :return: User data
        """
        try:
            graph = facebook.GraphAPI(access_token=token)
            user_data = graph.get_object(id="me",
                                         fields=", ".join(self.permissions))
            return self._normalize_user_data(user_data)
        except facebook.GraphAPIError as error:
            raise FacebookException(detail=error.message)
