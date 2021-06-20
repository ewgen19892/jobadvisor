"""Test base auth backend."""
from unittest.mock import patch

from faker import Faker
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from tests.factories import (
    FacebookTokenFactory,
    GoogleTokenFactory,
    LinkedinTokenFactory,
    TokenFactory,
    UserFactory,
)

from jobadvisor.authentication import backends
from jobadvisor.authentication.serializers import ConvertTokenSerializer
from jobadvisor.users.models import User


class ConvertTokenSerializerTestCase(APITestCase):
    """Test convert token serializer."""

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Set up data.

        :return: None
        """
        cls.serializer = ConvertTokenSerializer()
        cls.user = UserFactory()

    def setUp(self) -> None:
        """
        Set up test-case.

        :return: None
        """
        self.fake = Faker()

    def test_convert_token_serializer_get_token_success(self) -> None:
        token = self.serializer.get_token(self.user)
        self.assertIsInstance(token, RefreshToken)

    def test_convert_token_serializer_validate_success(self) -> None:
        with patch.object(ConvertTokenSerializer, "get_user",
                          return_value=(UserFactory(), False)):
            serializer = ConvertTokenSerializer(data=TokenFactory())
            serializer.is_valid()
            self.assertTrue(serializer.is_valid())

    def test_convert_token_serializer_get_facebook_user_success(self) -> None:
        with patch.object(backends.FacebookBackend, "get_user",
                          return_value=(UserFactory(), False)):
            data: dict = FacebookTokenFactory()
            serializer = ConvertTokenSerializer(data=data)
            user, is_created = serializer.get_user(**data)
            self.assertIsInstance(user, User)

    def test_convert_token_serializer_get_google_user_success(self) -> None:
        with patch.object(backends.GoogleBackend, "get_user",
                          return_value=(UserFactory(), False)):
            data: dict = GoogleTokenFactory()
            serializer = ConvertTokenSerializer(data=data)
            user, is_created = serializer.get_user(**data)
            self.assertIsInstance(user, User)

    def test_convert_token_serializer_get_linkedin_user_success(self) -> None:
        with patch.object(backends.LinkedinBackend, "get_user",
                          return_value=(UserFactory(), False)):
            data: dict = LinkedinTokenFactory()
            serializer = ConvertTokenSerializer(data=data)
            user, is_created = serializer.get_user(**data)
            self.assertIsInstance(user, User)
