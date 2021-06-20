from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import CategoryFactory, UserFactory


class CategoryListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return: None
        """
        cls.user = UserFactory()
        cls.category = CategoryFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return: None
        """
        self.client.force_authenticate(user=self.user)
        self.url = reverse("polls:category_list")

    def test_company_list_success(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CategoryDetailsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return: None
        """
        cls.user = UserFactory()
        cls.category = CategoryFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return: None
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("polls:category_detail",
                           kwargs={"pk": self.category.pk})

    def test_category_detail_success(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
