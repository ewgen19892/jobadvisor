from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import (
    CompanyFactory,
    JobFactory,
    PositionFactory,
    UserFactory,
)


class JobListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory()
        cls.position = PositionFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.job_stub = JobFactory.stub(company=self.company,
                                        position=self.position)
        self.url = reverse("users:job_list")

    def test_job_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_job_create_success(self):
        data = {
            "company": self.job_stub.company.pk,
            "position": self.job_stub.position.pk,
            "salary": self.job_stub.salary,
            "started_at": self.job_stub.started_at,
            "finished_at": self.job_stub.finished_at,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_job_create_bad_request(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class JobDetailsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.job = JobFactory(owner=cls.user)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.job_stub = JobFactory.stub(company=self.job.company,
                                        position=self.job.position)
        self.url = reverse("users:job_detail",
                           kwargs={"pk": self.job.pk})

    def test_job_detail_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_job_update_success(self):
        data = {
            "salary": self.job_stub.salary,
            "started_at": self.job_stub.started_at,
            "finished_at": self.job_stub.finished_at,
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_job_update_bad_request(self):
        data = {
            "salary": None,
            "started_at": self.fake.pyfloat(positive=True),
            "finished_at": self.fake.sentence(nb_words=8),
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_job_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_job_delete_permission_denied(self):
        another_user = UserFactory()
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
