from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import (
    CompanyFactory,
    IndustryFactory,
    SubscriptionFactory,
    UserFactory,
)


class CompanyListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory(level=2)
        cls.industry = IndustryFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.company_stub = CompanyFactory.stub(owner=self.user,
                                                industry=self.industry,
                                                logo=None)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("companies:company_list")

    def test_company_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_create_success(self):
        data = {
            "owner": self.company_stub.owner.pk,
            "name": self.company_stub.name,
            "industry": self.company_stub.industry.pk,
            "website": self.company_stub.website,
            "size": self.company_stub.size,
            "founded": self.company_stub.founded,
            "description": self.company_stub.description,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_company_create_bad_request(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CompanyDetailsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory(level=2)
        cls.company = CompanyFactory(owner=cls.user)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.company_stub = CompanyFactory.stub(owner=self.company.owner,
                                                industry=self.company.industry,
                                                logo=None)
        self.subscription = SubscriptionFactory(company=self.company)
        self.url = reverse("companies:company_detail",
                           kwargs={"pk": self.company.pk})

    def test_company_detail_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_update_success(self):
        data = {
            "owner": self.company_stub.owner.pk,
            "name": self.company_stub.name,
            "industry": self.company_stub.industry.pk,
            "website": self.company_stub.website,
            "size": self.company_stub.size,
            "founded": self.company_stub.founded,
            "description": self.company_stub.description,
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_company_update_bad_request(self):
        data = {
            "company": None,
            "speciality": self.fake.pyfloat(positive=True),
            "experience": self.fake.sentence(nb_words=8),
            "owner": self.user.pk,
            "name": self.fake.text(max_nb_chars=80),
            "industry": None,
            "website": self.fake.url(),
            "size": self.fake.sentence(nb_words=8),
            "founded": self.fake.date(),
            "description": self.fake.paragraph(),
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_company_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
