from django.http import HttpRequest

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.test import APITestCase
from tests.factories import CompanyFactory, SubscriptionFactory, UserFactory

from jobadvisor.companies.exceptions import (
    NoActiveSubscription,
    NoRequiredSubscription,
    NotWorker,
)
from jobadvisor.companies.permissions import CompanyPermission


class CompanyPermissionTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        SetUp test data.

        :return: None
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory(owner=cls.user)
        cls.permission = CompanyPermission()
        cls.view = GenericAPIView()
        cls.request = Request(HttpRequest())

    def setUp(self) -> None:
        self.request.user = self.user
        self.request.method = "PATCH"

    def test_company_permission_safe_success(self) -> None:
        self.request.method = "GET"
        self.assertTrue(self.permission.has_object_permission(self.request,
                                                              self.view,
                                                              self.company))

    def test_company_permission_not_safe_success(self) -> None:
        SubscriptionFactory(company=self.company, plan=1)
        self.assertTrue(self.permission.has_object_permission(self.request,
                                                              self.view,
                                                              self.company))

    def test_company_permission_no_worker(self) -> None:
        self.request.user = UserFactory()
        with self.assertRaises(NotWorker):
            self.permission.has_object_permission(self.request,
                                                  self.view,
                                                  self.company)

    def test_company_permission_no_subscription(self) -> None:
        self.company.subscriptions.all().delete()
        with self.assertRaises(NoActiveSubscription):
            self.permission.has_object_permission(self.request,
                                                  self.view,
                                                  self.company)
