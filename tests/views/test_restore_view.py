from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import UserFactory


class UserRestoreTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()

    def test_users_restore_request_success(self):
        data = {
            "email": self.user.email,
        }
        self.url = reverse("users:user_restore_request")
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], self.user.first_name)

    def test_users_restore_request_bad_request(self):
        data = {
            "first_name": self.user.first_name,
        }
        self.url = reverse("users:user_restore_request")
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_restore_finish_success(self):
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.url = reverse("users:user_restore_finish",
                           kwargs={"uid": uid, "token": token})
        data = {
            "password": self.fake.password(),
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_restore_finish_not_found(self):
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(
            force_bytes(self.fake.pyint(min_value=self.user.pk)))
        self.url = reverse("users:user_restore_finish",
                           kwargs={"uid": uid, "token": token})
        data = {
            "password": self.fake.password(),
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_users_restore_finish_invalid_token(self):
        token = self.fake.md5(raw_output=False)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.url = reverse("users:user_restore_finish",
                           kwargs={"uid": uid, "token": token})
        data = {
            "password": self.fake.password(),
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
