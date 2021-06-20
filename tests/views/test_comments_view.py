"""Comment tests."""
from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import (
    CommentedInterviewFactory,
    CommentedReviewFactory,
    InterviewFactory,
    ReviewFactory,
    SubscriptionFactory,
    UserFactory,
)


class CommentReviewTestCase(APITestCase):
    """Test commenting review"""

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.review = ReviewFactory()
        cls.company = cls.review.company
        cls.company.workers.add(cls.user)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.comment_stub = CommentedReviewFactory.stub(
            content_object=self.review)
        self.subscription = SubscriptionFactory(company=self.company)
        self.url = reverse("reviews:review_comment",
                           kwargs={"pk": self.review.pk})

    def test_comment_review_create_success(self):
        data = {
            "text": self.comment_stub.text,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_review_create_permission_denied(self):
        self.company.subscriptions.all().delete()
        data = {
            "text": self.comment_stub.text,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_review_create_bad_request(self):
        data = {
            "text": None,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CommentInterviewTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.interview = InterviewFactory()
        cls.company = cls.interview.company
        cls.company.workers.add(cls.user)
        cls.subscription = SubscriptionFactory(company=cls.company)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.comment_stub = CommentedInterviewFactory.stub(
            content_object=self.interview)
        self.url = reverse("reviews:interview_comment",
                           kwargs={"pk": self.interview.pk})

    def test_comment_interview_create_success(self):
        data = {
            "text": self.comment_stub.text,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_interview_create_bad_request(self):
        data = {
            "text": None,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_interview_create_permission_denied(self):
        self.company.subscriptions.all().delete()
        data = {
            "text": self.comment_stub.text,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
