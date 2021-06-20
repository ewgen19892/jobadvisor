"""Companies views."""
from django.db.models import Avg
from django.db.models.functions import Coalesce

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.common.pagination import JobAdvisorPagination
from jobadvisor.common.permissions import OwnerPermission
from jobadvisor.companies.filters import CompanyFilter
from jobadvisor.companies.models import Company
from jobadvisor.companies.permissions import CompanyPermission
from jobadvisor.companies.serializers import CompanySerializer


class CompanyList(GenericAPIView, ListModelMixin, CreateModelMixin):
    """Company list view."""

    serializer_class = CompanySerializer
    queryset = Company.objects.annotate(rate=Coalesce(Avg("reviews__rate"), 0))
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, CompanyPermission)
    filter_backends: tuple = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = CompanyFilter
    search_fields: tuple = ("name", "description")
    ordering_fields = ("rate",)
    pagination_class = JobAdvisorPagination

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get company list.

        :param request: Request
        :return: List of companies
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create the company.

        :param request: Request
        :return: New company
        """
        return self.create(request, *args, **kwargs)


class CompanyDetail(GenericAPIView,
                    RetrieveModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin):
    """Company detail view."""

    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes: tuple = (
        IsAuthenticatedOrReadOnly,
        OwnerPermission,
        CompanyPermission,
    )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the company.

        :param request: Request
        :return: Company instance
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Partial update the company.

        :param request: Request
        :return: Updated company
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Delete the company.

        :param request: Request
        :return: No Content
        """
        return self.destroy(request, *args, **kwargs)
