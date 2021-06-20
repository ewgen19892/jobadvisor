"""Base auth backend."""
import uuid
from typing import Tuple

from django.core.files.base import ContentFile

import requests

from jobadvisor.users.models import User


class BaseBackend:
    """Base auth backend."""

    @staticmethod
    def update_photo(url: str, user: User) -> None:
        """
        Upload user photo from social network.

        :param url: Photo URL.
        :param user: User
        :return: None
        """
        try:
            response = requests.get(url, allow_redirects=True)
        except requests.RequestException:
            return None
        if response.status_code == 200:
            content_type = response.headers.get("content-type", "jpg")
            if content_type:
                content_type = content_type.split("/")[-1]
            file_name = f"{uuid.uuid4()}.{content_type}"
            file = ContentFile(response.content)
            user.photo.save(file_name, file, save=True)
        return None

    def get_user_data(self, token: str) -> dict:
        """
        Get user data by token.

        :param token: Access token.
        :return: User
        """
        raise NotImplementedError("`get_user_data()` must be implemented.")

    def get_user(self, token: str) -> Tuple[User, bool]:
        """
        Get user by access token.

        :param token: access token
        :return: User
        """
        user_data = self.get_user_data(token)
        photo_url = user_data["photo_url"]
        user_data.pop("photo_url")
        is_created = False
        try:
            user = User.objects.get(email=user_data.get("email"))
        except User.DoesNotExist:
            user = User.objects.create_user(is_active=True, **user_data)
            BaseBackend.update_photo(url=photo_url, user=user)
            is_created = True
        return user, is_created
