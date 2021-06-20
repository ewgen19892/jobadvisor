from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import CompanyFactory, JobFactory, UserFactory

from jobadvisor.companies.models import Position


class SalaryListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory()
        for _ in range(10):
            JobFactory(company=cls.company)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:salaries_list")

    def test_salary_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        positions_count = Position.objects.filter(jobs__company=self.company).count()
        self.assertEqual(int(response.get("X-Total")), positions_count)
