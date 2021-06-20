from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import QuestionFactory, UserFactory, VariantFactory

from jobadvisor.polls.serializers import VariantSerializer


class VariantListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return: None
        """
        cls.user = UserFactory()
        cls.question = QuestionFactory()
        cls.variant = VariantFactory(
            question=cls.question,
            is_positive=True,
            weight=1,
        )

    def setUp(self) -> None:
        """
        Setup tests.

        :return: None
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("polls:variant_list")

    def test_variant_list_success(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_variant_list_filter_by_question_success(self) -> None:
        response = self.client.get(
            self.url,
            data={"question": self.question.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(VariantSerializer(self.variant).data, response.data)

    def test_variant_list_filter_by_question_fail(self) -> None:
        response = self.client.get(
            self.url,
            data={"question": self.fake.random_int(min=9999)},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VariantDetailsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return: None
        """
        cls.user = UserFactory()
        cls.variant = VariantFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return: None
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("polls:variant_detail",
                           kwargs={"pk": self.variant.pk})

    def test_variant_detail_success(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
