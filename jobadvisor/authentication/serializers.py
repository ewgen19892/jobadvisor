"""Authentication serializers."""
from typing import Tuple

from django.http import QueryDict

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from jobadvisor.authentication.backends import (
    FacebookBackend,
    GoogleBackend,
    LinkedinBackend,
)
from jobadvisor.authentication.backends.base import BaseBackend
from jobadvisor.users.models import User
from jobadvisor.users.serializers import UserSerializer


class ConvertTokenSerializer(serializers.Serializer):
    """Convert token serializer."""

    FACEBOOK: str = "facebook"
    GOOGLE: str = "google"
    LINKEDIN: str = "linkedin"

    BACKENDS: tuple = (
        (FACEBOOK, FacebookBackend),
        (GOOGLE, GoogleBackend),
        (LINKEDIN, LinkedinBackend),
    )

    token: str = serializers.CharField()
    backend: str = serializers.ChoiceField(choices=BACKENDS)

    def get_token(self, user: User) -> RefreshToken:
        """
        Get token for the user.

        :param user: User
        :return: Refresh token
        """
        token: RefreshToken = RefreshToken.for_user(user)
        token["user"] = UserSerializer(user, context=self.context).data
        return token

    @classmethod
    def get_user(cls, token: str, backend: str) -> Tuple[User, bool]:
        """
        Get user.

        :param token: Access token
        :param backend: Backend name
        :return: User
        """
        auth_backend: BaseBackend = dict(cls.BACKENDS)[backend]()
        return auth_backend.get_user(token)

    def validate(self, attrs: QueryDict) -> dict:
        """
        Validate user data.

        :param attrs: Access token and backend name.
        :return: Access and refresh tokens
        """
        super().validate(attrs)
        user, is_created = self.get_user(**attrs)
        refresh: RefreshToken = self.get_token(user)
        data: dict = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user, context=self.context).data,
            "is_created": is_created,
        }
        return data


class ObtainTokenPairSerializer(TokenObtainPairSerializer):
    """Obtain token pair serializer."""

    def get_token(self, user: User) -> RefreshToken:
        """
        Get token for the user.

        :param user: User
        :return: Refresh token
        """
        token: RefreshToken = RefreshToken.for_user(user)
        token["user"] = UserSerializer(user, context=self.context).data
        return token

    def validate(self, attrs: dict) -> dict:
        """
        Validate serializer.

        :param attrs:
        :return:
        """
        super().validate(attrs)
        refresh: RefreshToken = self.get_token(self.user)
        data: dict = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(self.user, context=self.context).data,
            "is_created": False,
        }
        return data
