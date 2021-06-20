from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import UserFactory


class UserListTestCase(APITestCase):

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
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:user_list")

    def test_users_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserDetailTestCase(APITestCase):

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
        self.client.force_authenticate(user=self.user)
        self.user_stub = UserFactory.stub()
        self.url = reverse("users:user_detail", kwargs={"pk": self.user.pk})

    def test_users_get_detail_success_pk(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_get_detail_success_me(self):
        self.url = reverse("users:user_detail", kwargs={"pk": "me"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_update_success(self):
        data = {
            "first_name": self.user_stub.first_name,
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_update_bad_request(self):
        data = {
            "photo": self.user_stub.first_name,
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_update_detail_permission_denied(self):
        another_user = UserFactory()
        self.url = reverse("users:user_detail", kwargs={"pk": another_user.pk})
        response = self.client.patch(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_delete_detail_permission_denied(self):
        another_user = UserFactory()
        self.url = reverse("users:user_detail", kwargs={"pk": another_user.pk})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
