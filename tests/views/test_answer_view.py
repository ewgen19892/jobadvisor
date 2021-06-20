from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import (
    AnswerFactory,
    CategoryFactory,
    CompanyFactory,
    QuestionFactory,
    UserFactory,
    VariantFactory,
)

from jobadvisor.polls.models import Answer
from jobadvisor.polls.serializers import AnswerSerializer


class AnswerListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return: None
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory()
        cls.category = CategoryFactory()
        cls.question = QuestionFactory(category=cls.category)
        cls.variant = VariantFactory(question=cls.question)
        cls.positive_variant = VariantFactory(
            question=cls.question,
            is_positive=True
        )
        cls.answer = AnswerFactory(
            company=cls.company,
            owner=cls.user,
            question=cls.question,
        )
        AnswerFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return: None
        """
        self.fake = Faker()
        self.answer_stub = AnswerFactory.stub(
            owner=self.user,
            company=self.company,
            question=self.question,
            variant=[self.variant.pk],
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse("polls:answer_list")
        self.data = {
            "owner": self.answer_stub.owner.pk,
            "company": self.answer_stub.company.pk,
            "question": self.answer_stub.question.pk,
            "variant": [self.positive_variant.pk],
        }

    def test_answer_list_success(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_answer_create_success(self) -> None:
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_answer_create_some_positive_variants(self) -> None:
        positive_variant_two = VariantFactory(
            question=self.question,
            is_positive=True
        )
        self.data["variant"] = \
            [self.positive_variant.pk, positive_variant_two.pk]
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_create_with_negative_and_positive_variants(self) -> None:
        negative_variant = VariantFactory(
            question=self.question,
            is_positive=False
        )
        self.data["variant"] = [self.positive_variant.pk, negative_variant.pk]
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_create_bad_request(self) -> None:
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_list_filter_by_user_success(self) -> None:
        response = self.client.get(self.url,
                                   data={"my": 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(AnswerSerializer(self.answer).data, response.data)

    def test_answer_list_filter_by_user_fail(self) -> None:
        response = self.client.get(self.url, data={"my": ""})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            AnswerSerializer(Answer.objects.all(), many=True).data,
            response.data,
        )

    def test_answer_list_filter_by_question_success(self) -> None:
        response = self.client.get(
            self.url,
            data={"question": self.question.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(AnswerSerializer(self.answer).data, response.data)

    def test_answer_list_filter_by_question_fail(self) -> None:
        response = self.client.get(
            self.url,
            data={"question": self.fake.random_int(min=9999)},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_list_filter_by_category_success(self) -> None:
        response = self.client.get(
            self.url,
            data={"category": self.category.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(AnswerSerializer(self.answer).data, response.data)

    def test_answer_list_filter_by_category_fail(self) -> None:
        response = self.client.get(
            self.url,
            data={"category": self.fake.random_int(min=self.category.pk + 1)},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_list_filter_by_company_success(self) -> None:
        response = self.client.get(
            self.url,
            data={"company": self.company.pk},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(AnswerSerializer(self.answer).data, response.data)

    def test_answer_list_filter_by_company_fail(self) -> None:
        response = self.client.get(
            self.url,
            data={"company": self.fake.random_int(min=9999)},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AnswerDetailsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return: None
        """
        cls.user = UserFactory()
        cls.my_answer = AnswerFactory(owner=cls.user)
        cls.another_answer = AnswerFactory()
        cls.variant = VariantFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return: None
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("polls:answer_detail",
                           kwargs={"pk": self.my_answer.pk})

    def test_answer_update_denied(self) -> None:
        url = reverse(
            "polls:answer_detail",
            kwargs={"pk": self.another_answer.pk}
        )
        response = self.client.patch(url, data={"text": "some text"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_answer_update_success(self) -> None:
        response = self.client.patch(
            self.url,
            data={"variant": [self.variant.pk]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Answer.objects.get(id=self.my_answer.pk).variant.first().pk,
            self.variant.pk
        )

    def test_answer_update_bad_request(self) -> None:
        response = self.client.patch(self.url, data={"question": None})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_detail_success(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_answer_delete_success(self) -> None:
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_answer_delete_permission_denied(self) -> None:
        url = reverse(
            "polls:answer_detail",
            kwargs={"pk": self.another_answer.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
