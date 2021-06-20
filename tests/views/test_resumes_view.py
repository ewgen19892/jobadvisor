from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import ResumeFactory, UserFactory


class ResumeListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.resume = ResumeFactory(owner=cls.user)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.resume_stub = ResumeFactory.stub(owner=self.resume.owner,
                                              file=None)
        self.url = reverse("users:resume_list")

    def test_resume_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resume_create_success(self):
        self.resume.delete()
        data = {
            "file": self.resume_stub.file,
            "experience": self.resume_stub.experience,
            "certificates": self.resume_stub.certificates,
            "description": self.resume_stub.description,
            "salary": self.resume_stub.salary,
            "skills": [],
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_resume_create_bad_request(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ResumeDetailsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.resume = ResumeFactory(owner=cls.user, file=None)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.resume_stub = ResumeFactory.stub(owner=self.resume.owner,
                                              file=None)
        self.url = reverse("users:resume_detail", kwargs={"pk": self.resume.pk})

    def test_resume_detail_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resume_update_success(self):
        data = {
            "file": self.resume_stub.file,
            "experience": self.resume_stub.experience,
            "certificates": self.resume_stub.certificates,
            "description": self.resume_stub.description,
            "salary": self.resume_stub.salary,
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resume_update_bad_request(self):
        data = {
            "file": None,
            "experience": self.fake.pyfloat(positive=True),
            "certificates": self.fake.sentence(nb_words=8),
            "description": self.fake.paragraph(),
            "salary": self.fake.sentence(nb_words=8),
            "skills": self.fake.random_int(min=1),
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resume_update_success_docx(self):
        with open('fixtures/test_file.docx', 'rb') as file:
            data = {
                "file": file,
            }
            response = self.client.patch(self.url, data=data,
                                         format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resume_update_success_pdf(self):
        with open('fixtures/test_file.pdf', 'rb') as file:
            data = {
                "file": file,
            }
            response = self.client.patch(self.url, data=data,
                                         format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resume_update_bad_request_file(self):
        with open('fixtures/test_file.txt', 'r') as file:
            data = {
                "file": file,
            }
            response = self.client.patch(self.url, data=data,
                                         format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resume_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_resume_delete_permission_denied(self):
        another_user = UserFactory()
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
