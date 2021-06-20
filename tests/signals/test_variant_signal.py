from rest_framework.test import APITestCase
from tests.factories import QuestionFactory, VariantFactory

from jobadvisor.polls.models import Variant


class VariantSignalTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        SetUp test data.

        :return: None
        """
        cls.question = QuestionFactory()

    def test_calculate_weight_some_negative_variant(self) -> None:
        VariantFactory(question=self.question, is_positive=False)
        VariantFactory(question=self.question, is_positive=False)

        negative_variant = Variant.objects.filter(
            question_id=self.question.id,
            is_positive=False
        )

        self.assertEqual(negative_variant.first().weight, 0.5)
        self.assertEqual(negative_variant.last().weight, 0.5)

    def test_calculate_weight_negative_variant(self) -> None:
        VariantFactory(question=self.question, is_positive=False)

        negative_variant = Variant.objects.get(
            question_id=self.question.id,
            is_positive=False
        )

        self.assertEqual(negative_variant.weight, 0)

    def test_calculate_weight_positive_variant(self) -> None:
        VariantFactory(question=self.question, is_positive=True)

        positive_variant = Variant.objects.get(
            question_id=self.question.id,
            is_positive=True
        )

        self.assertEqual(positive_variant.weight, 1)

    def test_recalculate_weight_del_some_negative_variant(self) -> None:
        VariantFactory(question=self.question, is_positive=False)
        VariantFactory(question=self.question, is_positive=False)
        VariantFactory(question=self.question, is_positive=False)
        VariantFactory(question=self.question, is_positive=False)

        negative_variant = Variant.objects.filter(
            question_id=self.question.id,
            is_positive=False
        )

        self.assertEqual(negative_variant.first().weight, 0.25)
        self.assertEqual(negative_variant.last().weight, 0.25)

        negative_variant.first().delete()
        negative_variant.last().delete()

        self.assertEqual(negative_variant.first().weight, 0.5)
        self.assertEqual(negative_variant.last().weight, 0.5)

    def test_recalculate_weight_del_negative_variant(self) -> None:
        VariantFactory(question=self.question, is_positive=False)
        VariantFactory(question=self.question, is_positive=False)

        negative_variant = Variant.objects.filter(
            question_id=self.question.id,
            is_positive=False
        )

        self.assertEqual(negative_variant.first().weight, 0.5)
        self.assertEqual(negative_variant.last().weight, 0.5)

        negative_variant.first().delete()

        self.assertEqual(negative_variant.first().weight, 0)

    def test_recalculate_weight_del_positive_variant(self) -> None:
        VariantFactory(question=self.question, is_positive=True)
        VariantFactory(question=self.question, is_positive=True)

        positive_variant = Variant.objects.filter(
            question_id=self.question.id,
            is_positive=True
        )

        self.assertEqual(positive_variant.first().weight, 1)
        self.assertEqual(positive_variant.last().weight, 1)

        positive_variant.first().delete()

        self.assertEqual(positive_variant.first().weight, 1)
