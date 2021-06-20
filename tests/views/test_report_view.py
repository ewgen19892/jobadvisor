from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import (
    InterviewFactory,
    ReportedInterviewFactory,
    ReportedReviewFactory,
    ReviewFactory,
    UserFactory,
)


class ReportReviewTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.review = ReviewFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.report_stub = ReportedReviewFactory.stub(
            content_object=self.review)
        self.url = reverse("reviews:review_report",
                           kwargs={"pk": self.review.pk})

    def test_report_create_success(self):
        data = {
            "text": self.report_stub.text,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_report_create_bad_request(self):
        data = {
            "text": None,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReportInterviewTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.interview = InterviewFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.report_stub = ReportedInterviewFactory.stub(
            content_object=self.interview)
        self.url = reverse("reviews:interview_report",
                           kwargs={"pk": self.interview.pk})

    def test_report_create_success(self):
        data = {
            "text": self.report_stub.text,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_report_create_bad_request(self):
        data = {
            "text": None,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
