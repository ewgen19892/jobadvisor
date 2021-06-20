from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import EducationFactory, InstituteFactory, UserFactory


class EducationListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.education = EducationFactory(owner=cls.user)
        cls.institute = InstituteFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.education_stub = EducationFactory.stub(institute=self.institute)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:education_list")

    def test_education_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_education_list_search_success(self):
        response = self.client.get(self.url, data={"owner": self.user.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["speciality"],
                         self.education.speciality)

    def test_education_list_search_fail(self):
        response = self.client.get(self.url,
                                   data={"owner": self.fake.random_int(min=9999)})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_education_create_success(self):
        data = {
            "graduated": self.education_stub.graduated,
            "speciality": self.education_stub.speciality,
            "institute": self.education_stub.institute.pk,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_education_create_bad_request(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EducationDetailsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.education = EducationFactory(owner=cls.user)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.education_stub = EducationFactory.stub()
        self.url = reverse("users:education_detail",
                           kwargs={"pk": self.education.pk})

    def test_education_detail_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_education_update_success(self):
        data = {
            "graduated": self.education_stub.graduated,
            "speciality": self.education_stub.speciality,
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_education_update_bad_request(self):
        data = {
            "graduated": None,
            "speciality": self.fake.pyfloat(positive=True),
            "experience": self.fake.sentence(nb_words=8),
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_education_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_education_delete_permission_denied(self):
        another_user = UserFactory()
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
