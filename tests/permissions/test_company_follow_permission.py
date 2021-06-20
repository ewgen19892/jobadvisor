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
from jobadvisor.companies.permissions import CompanyFollowPermission


class CompanyFollowPermissionTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        SetUp test data.

        :return: None
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory(owner=cls.user)
        cls.permission = CompanyFollowPermission()
        cls.view = GenericAPIView()
        cls.request = Request(HttpRequest())

    def setUp(self) -> None:
        self.request.user = self.user
        self.request.method = "GET"

    def test_company_follow_permission_success_get(self) -> None:
        self.company.subscriptions.all().delete()
        SubscriptionFactory(company=self.company, plan=3)
        self.assertTrue(self.permission.has_object_permission(self.request,
                                                              self.view,
                                                              self.company))

    def test_company_follow_permission_success_post(self) -> None:
        self.request.user = None
        self.request.method = None
        self.assertTrue(self.permission.has_object_permission(self.request,
                                                              self.view,
                                                              self.company))

    def test_company_follow_permission_success_delete(self) -> None:
        self.request.user = None
        self.request.method = None
        self.assertTrue(self.permission.has_object_permission(self.request,
                                                              self.view,
                                                              self.company))

    def test_company_follow_permission_no_worker(self) -> None:
        self.request.user = UserFactory()
        with self.assertRaises(NotWorker):
            self.permission.has_object_permission(self.request,
                                                  self.view,
                                                  self.company)

    def test_company_follow_permission_no_required_subscription(self) -> None:
        SubscriptionFactory(company=self.company, plan=1)
        with self.assertRaises(NoRequiredSubscription):
            self.permission.has_object_permission(self.request,
                                                  self.view,
                                                  self.company)

    def test_company_follow_permission_no_subscription(self) -> None:
        self.company.subscriptions.all().delete()
        with self.assertRaises(NoActiveSubscription):
            self.permission.has_object_permission(self.request,
                                                  self.view,
                                                  self.company)
