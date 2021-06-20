"""Linkedin auth backend."""
import os
from typing import Dict

from django.utils.translation import ugettext_lazy as _

import requests
from rest_framework import status
from rest_framework.exceptions import APIException

from jobadvisor.authentication.backends.base import BaseBackend


class LinkedinException(APIException):
    """Linkedin exception."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Linkedin exception")


class BadAuthCodeException(APIException):
    """Bad authorization code exception."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Bad authorization code")


class PermissionException(LinkedinException):
    """Linkedin permission exception."""

    default_detail = _("No required permissions")


class LinkedinBackend(BaseBackend):
    """Linkedin backend."""

    host: str = "https://api.linkedin.com"
    token: str = ""
    headers: Dict[str, str] = {
        "Authorization": f"Bearer {token}"
    }
    _client_id = os.getenv("LINKEDIN_ID")
    _client_secret = os.getenv("LINKEDIN_SECRET")
    _redirect_uri = os.getenv("LINKEDIN_REDIRECT")

    @staticmethod
    def _normalize_user_data(user_data: dict) -> dict:
        """
        Normalize user data.

        :param user_data: User data from Linkedin
        :return: normalized user data.
        """
        try:
            data = {
                "first_name": user_data["localizedFirstName"],
                "last_name": user_data["localizedLastName"],
                "email": user_data["elements"][0]["handle~"]["emailAddress"],
                "photo_url": None,
            }
            return data
        except KeyError:
            raise PermissionException

    def _auth(self, auth_code: str) -> None:
        """
        Get user access token by authorization code.

        :param auth_code: Authorization code
        """
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self._redirect_uri,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        response = requests.post(
            "https://www.linkedin.com/oauth/v2/accessToken", data=data)
        if not response.status_code == 200:
            raise BadAuthCodeException
        self.token = response.json().get("access_token")
        self.headers["Authorization"] = f"Bearer {self.token}"

    def _get_me(self) -> dict:
        """
        Get user.

        :return: User data
        """
        permissions: tuple = (
            "id",
            "localizedFirstName",
            "localizedLastName",
        )
        params = {
            "projection": "({})".format(",".join(permissions))
        }
        response = requests.get(f"{self.host}/v2/me",
                                headers=self.headers, params=params)
        if not response.status_code == 200:
            raise PermissionException
        return response.json()

    def _get_email(self) -> dict:
        """
        Get email.

        :return: User email
        """
        permissions: tuple = (
            "elements*(handle~)",
        )
        params = {
            "q": "members",
            "projection": "({})".format(",".join(permissions)),
        }
        response = requests.get(f"{self.host}/v2/emailAddress",
                                headers=self.headers, params=params)
        if not response.status_code == 200:
            raise PermissionException
        return response.json()

    def get_user_data(self, token: str) -> dict:
        """
        Get user data.

        :param token: Access token for GraphAPI
        :return: User data
        """
        self._auth(token)
        user_data = self._get_me()
        user_data.update(self._get_email())
        return self._normalize_user_data(user_data)
