import pytest
from rest_framework.test import APITestCase
from tests.factories import (
    AnswerFactory,
    CompanyFactory,
    QuestionFactory,
    ReviewFactory,
    SubscriptionFactory,
    UserFactory,
    VariantFactory,
)

from jobadvisor.companies.exceptions import NoRequiredSubscription
from jobadvisor.notifications.models import Message
from jobadvisor.reviews.models import Review


@pytest.mark.django_db
def test_company_notify_workers_with_owner(mocker, company) -> None:
    mocker.spy(Message.objects, "bulk_create")
    company.notify_workers("", Message.INFO)
    assert Message.objects.bulk_create.call_count == 1


@pytest.mark.django_db
def test_company_notify_workers_without_owner(mocker, company) -> None:
    company.owner = None
    mocker.spy(Message.objects, "bulk_create")
    company.notify_workers("", Message.INFO)
    assert Message.objects.bulk_create.call_count == 0


class CompanyModelTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        SetUp test data.

        :return: None
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory(owner=cls.user)
        cls.question = QuestionFactory()
        cls.variant = VariantFactory(question=cls.question, is_positive=True)
        cls.answer = AnswerFactory(
            question=cls.question,
            variant=[cls.variant],
            company=cls.company
        )

    def test_company_poll_results_success(self) -> None:
        result = {
            "category": self.question.category,
            "result": 100.0,
        }
        self.assertIn(result, self.company.poll_results)

    def test_company_rating_success(self) -> None:
        ReviewFactory(company=self.company, rate=0)
        ReviewFactory(company=self.company, rate=5)
        self.assertEqual(
            {"rating": 2.5, "count": Review.objects.count()},
            self.company.rating
        )

    def test_company_name_success(self) -> None:
        self.assertEqual(str(self.company), self.company.name)

    def test_company_logo_img_success(self) -> None:
        logo_img = f"<img src='{self.company.logo.url}' width='100' height='50'/>"
        self.assertEqual(self.company.logo_img, logo_img)

    def test_company_owner_phone_success(self) -> None:
        self.assertEqual(self.company.owner_phone, self.company.owner.phone)

    def test_company_owner_phone_fail(self) -> None:
        company = CompanyFactory(owner=None)
        self.assertEqual(company.owner_phone, None)

    def test_company_owner_email_success(self) -> None:
        self.assertEqual(self.company.owner_email, self.company.owner.email)

    def test_company_owner_email_fail(self) -> None:
        company = CompanyFactory(owner=None)
        self.assertEqual(company.owner_email, None)

    def test_company_admin_url(self) -> None:
        self.assertIs(type(self.company.get_admin_url()), str)

    def test_company_has_perm_no_subscription(self) -> None:
        self.company.subscriptions.all().delete()
        self.assertFalse(
            self.company.has_perm(1, self.user, raise_exception=False))
        self.assertFalse(
            self.company.has_perm(2, self.user, raise_exception=False))
        self.assertFalse(
            self.company.has_perm(3, self.user, raise_exception=False))

    def test_company_has_perm_no_worker(self) -> None:
        user = UserFactory()
        self.assertFalse(
            self.company.has_perm(1, user, raise_exception=False))
        self.assertFalse(
            self.company.has_perm(2, user, raise_exception=False))
        self.assertFalse(
            self.company.has_perm(3, user, raise_exception=False))

    def test_company_has_perm_first_success(self) -> None:
        SubscriptionFactory(company=self.company, plan=1)
        self.assertTrue(
            self.company.has_perm(1, self.user, raise_exception=False))
        self.assertFalse(
            self.company.has_perm(2, self.user, raise_exception=False))
        self.assertFalse(
            self.company.has_perm(3, self.user, raise_exception=False))

    def test_company_has_perm_second_success(self) -> None:
        SubscriptionFactory(company=self.company, plan=2)
        self.assertTrue(
            self.company.has_perm(1, self.user, raise_exception=False))
        self.assertTrue(
            self.company.has_perm(2, self.user, raise_exception=False))
        self.assertFalse(
            self.company.has_perm(3, self.user, raise_exception=False))

    def test_company_has_perm_third_success(self) -> None:
        SubscriptionFactory(company=self.company, plan=3)
        self.assertTrue(
            self.company.has_perm(1, self.user, raise_exception=False))
        self.assertTrue(
            self.company.has_perm(2, self.user, raise_exception=False))
        self.assertTrue(
            self.company.has_perm(3, self.user, raise_exception=False))

    def test_company_has_perm_no_subscription_required(self) -> None:
        SubscriptionFactory(company=self.company, plan=1)
        with self.assertRaises(NoRequiredSubscription):
            self.company.has_perm(2, self.user)
        with self.assertRaises(NoRequiredSubscription):
            self.company.has_perm(3, self.user)
