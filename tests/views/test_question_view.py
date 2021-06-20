from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import CategoryFactory, QuestionFactory, UserFactory

from jobadvisor.polls.serializers import QuestionSerializer


class QuestionListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return: None
        """
        cls.user = UserFactory()
        cls.category = CategoryFactory()
        cls.question = QuestionFactory(category=cls.category)

    def setUp(self) -> None:
        """
        Setup tests.

        :return: None
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("polls:question_list")

    def test_question_list_success(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_question_list_filter_by_category_success(self) -> None:
        response = self.client.get(
            self.url,
            data={"category": self.category.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(QuestionSerializer(self.question).data, response.data)

    def test_question_list_filter_by_category_fail(self) -> None:
        response = self.client.get(
            self.url,
            data={"category": self.fake.random_int(min=9999)},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class QuestionDetailsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return: None
        """
        cls.user = UserFactory()
        cls.question = QuestionFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return: None
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("polls:question_detail",
                           kwargs={"pk": self.question.pk})

    def test_question_detail_success(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
