"""Salaries views."""
from django.db.models import Avg, Count, Max, Min

from django_filters.rest_framework import DjangoFilterBackend
from requests import Request
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from jobadvisor.companies.models import Position
from jobadvisor.users.filters import SalaryFilter
from jobadvisor.users.serializers import SalarySerializer


class SalaryList(GenericAPIView, ListModelMixin):
    """Salary list view."""

    serializer_class = SalarySerializer
    queryset = Position.objects.annotate(avg=Avg("jobs__salary"),
                                         min=Min("jobs__salary"),
                                         max=Max("jobs__salary"),
                                         count=Count("jobs")).all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    filter_backends: tuple = (
        SearchFilter,
        DjangoFilterBackend,
    )
    filterset_class = SalaryFilter
    search_fields: tuple = ("jobs__position__name",)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get salaries list.

        :param request: Request
        :return: List of salaries
        """
        return self.list(request, *args, **kwargs)
