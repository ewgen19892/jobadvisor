from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase


class JobAdviserTestCase(APITestCase):

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.url = reverse("index")

    def test_index_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
