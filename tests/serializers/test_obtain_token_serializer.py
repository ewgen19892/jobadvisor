"""Test obtain token serializer."""
from django.urls import reverse

from faker import Faker
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APITestCase
from tests.factories import UserFactory

from jobadvisor.authentication.serializers import ObtainTokenPairSerializer
from jobadvisor.users.models import User


class ObtainTokenSerializerTestCase(APITestCase):
    """Test obtain token serializer."""

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Set up data.

        :return: None
        """
        cls.user = UserFactory()
        cls.serializer = ObtainTokenPairSerializer

    def setUp(self) -> None:
        """
        Set up test-case.

        :return: None
        """
        self.fake = Faker()
        self.password = self.fake.password()
        self.email = self.fake.email()
        self.user = User.objects.create_user(email=self.email,
                                             password=self.password)
        self.user.is_active = True
        self.user.save()
        self.url = reverse("authentication:obtain_token")

    def test_obtain_token_success(self) -> None:
        serializer = self.serializer(
            data={"email": self.email, "password": self.password})
        self.assertTrue(serializer.is_valid())

    def test_obtain_token_fail_password(self) -> None:
        serializer = self.serializer(
            data={"email": self.email, "password": self.fake.password()})
        with self.assertRaises(AuthenticationFailed):
            serializer.is_valid()

    def test_obtain_token_fail_email(self) -> None:
        serializer = self.serializer(
            data={"email": self.fake.email(), "password": self.password})
        with self.assertRaises(AuthenticationFailed):
            serializer.is_valid()
