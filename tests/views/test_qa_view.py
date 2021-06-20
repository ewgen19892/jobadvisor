from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import InterviewFactory, QAFactory, UserFactory


class QAListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.interview = InterviewFactory(owner=cls.user)
        cls.qa = QAFactory(interview=cls.interview)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.qa_stub = QAFactory.stub(interview=self.interview)
        self.url = reverse("reviews:qas_list")

    def test_qa_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_qa_list_filter_success(self):
        response = self.client.get(self.url,
                                   data={"interview": self.interview.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.interview.qas.count())

    def test_qa_create_success(self):
        data = {
            "interview": self.qa_stub.interview.pk,
            "question": self.qa_stub.question,
            "answer": self.qa_stub.answer,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_qa_create_bad_request(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_qa_create_unauthorized(self):
        self.client.force_authenticate(user=UserFactory())
        data = {
            "interview": self.qa_stub.interview.pk,
            "question": self.qa_stub.question,
            "answer": self.qa_stub.answer,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class QADetailsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.interview = InterviewFactory(owner=cls.user)
        cls.qa = QAFactory(interview=cls.interview)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.qa_stub = QAFactory.stub(interview=self.interview)
        self.url = reverse("reviews:qas_detail",
                           kwargs={"pk": self.qa.pk})

    def test_qa_detail_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_qa_update_success(self):
        data = {
            "interview": self.qa_stub.interview.pk,
            "question": self.qa_stub.question,
            "answer": self.qa_stub.answer,
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_qa_update_bad_request(self):
        data = {
            "interview": None,
            "question": self.qa_stub.question,
            "answer": self.qa_stub.answer,
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_qa_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_qa_delete_permission_denied(self):
        another_user = UserFactory()
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
