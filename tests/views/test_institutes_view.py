from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import InstituteFactory, UserFactory

from jobadvisor.users.serializers import InstituteSerializer


class InstituteListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.institute = InstituteFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.institute_stub = InstituteFactory.stub()
        self.url = reverse("users:institute_list")

    def test_institute_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_institute_list_search_success(self):
        response = self.client.get(self.url,
                                   data={"search": self.institute.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         [InstituteSerializer(instance=self.institute).data])

    def test_institute_list_search_fail(self):
        response = self.client.get(self.url, data={"search": self.fake.iban()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_institute_create_success(self):
        data = {
            "name": self.institute_stub.name
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_institute_create_bad_request(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
