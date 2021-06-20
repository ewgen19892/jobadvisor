from django.urls import reverse

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import IndustryFactory, UserFactory

from jobadvisor.companies.serializers import IndustrySerializer
from jobadvisor.companies.views import IndustryList


class IndustryListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.industry = IndustryFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("companies:industry_list")

    def test_industry_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_industry_list_search_fail(self):
    #     response = self.client.get(self.url, data={"search": self.fake.iban()})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertNotIn(IndustrySerializer(self.industry).data, response.data)


@pytest.mark.django_db
def test_industry_list_success(rf, industries):
    request = rf.get("")
    response = IndustryList.as_view()(request)
    assert int(response["X-Total"]) == len(industries)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_industry_list_search_success(rf, industries, industry):
    request = rf.get("", data={"search": industry.name})
    response = IndustryList.as_view()(request)
    assert response.status_code == status.HTTP_200_OK
    assert IndustrySerializer(industry).data in response.data
