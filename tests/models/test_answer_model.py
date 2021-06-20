from rest_framework.test import APITestCase
from tests.factories import AnswerFactory, QuestionFactory, VariantFactory


class AnswerModelTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        SetUp test data.

        :return: None
        """
        cls.question = QuestionFactory()
        cls.positive_variant = VariantFactory(
            is_positive=True,
            question=cls.question
        )
        cls.answer = AnswerFactory(question=cls.question)

    def test_answer_name(self) -> None:
        self.assertEqual(
            str(self.answer),
            f"{self.answer.owner.get_full_name()}. {self.answer.weight}"
        )

    def test_answer_weight_positive_variant(self) -> None:
        VariantFactory(is_positive=False, question=self.question)
        answer = AnswerFactory(variant=[self.positive_variant])

        self.assertEqual(answer.weight, 1)

    def test_answer_weight_negative_variant(self) -> None:
        negative_variant = VariantFactory(
            is_positive=False,
            question=self.question
        )
        answer = AnswerFactory(variant=[negative_variant])

        self.assertEqual(answer.weight, 0)

    def test_answer_weight_two_negative_variants(self) -> None:
        VariantFactory(is_positive=False, question=self.question)
        negative_variant = VariantFactory(
            is_positive=False,
            question=self.question
        )
        answer = AnswerFactory(variant=[negative_variant])

        self.assertEqual(answer.weight, 0.5)

    def test_answer_weight_some_negative_variants(self) -> None:
        VariantFactory(is_positive=False, question=self.question)
        VariantFactory(is_positive=False, question=self.question)
        VariantFactory(is_positive=False, question=self.question)
        negative_variant = VariantFactory(
            is_positive=False,
            question=self.question
        )
        answer = AnswerFactory(variant=[negative_variant])

        self.assertEqual(answer.weight, 0.75)
