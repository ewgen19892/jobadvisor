"""Vacancy views."""
from datetime import datetime

from django.db.models import QuerySet

import pytz
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.companies.exceptions import MaxTopVacancies
from jobadvisor.companies.filters import VacancyFilter
from jobadvisor.companies.models import Vacancy
from jobadvisor.companies.permissions import (
    VacancyPermission,
    VacancyRespondedPermission,
    VacancyResponsePermission,
    VacancyTopPermission,
)
from jobadvisor.companies.serializers import VacancySerializer
from jobadvisor.users.serializers import UserSerializer


class VacancyList(GenericAPIView, ListModelMixin, CreateModelMixin):
    """Vacancy list view."""

    serializer_class = VacancySerializer
    queryset = Vacancy.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    filter_backends: tuple = (
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    )
    filterset_class = VacancyFilter
    search_fields: tuple = (
        "description",
        "location",
        "company__name",
        "position__name",
    )
    ordering_fields: tuple = (
        "created_at",
        "salary",
        "experience",
    )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get vacancy list.

        :param request: Request
        :return: List of vacancies
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create the vacancy.

        :param request: Request
        :return: New vacancy
        """
        return self.create(request, *args, **kwargs)


class VacancyDetail(GenericAPIView,
                    RetrieveModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin):
    """Vacancy detail view."""

    serializer_class = VacancySerializer
    queryset = Vacancy.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, VacancyPermission)

    def get_queryset(self) -> QuerySet:
        """
        Get queryset.

        :return:
        """
        queryset = super().get_queryset()
        return queryset.filter(deleted_at__isnull=True)

    def perform_destroy(self, instance: Vacancy):
        """
        Delete vacancy.

        :param instance:
        :return:
        """
        instance.deleted_at = datetime.now(pytz.UTC)
        instance.save()

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the vacancy.

        :param request: Request
        :return: Vacancy
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Partial update the vacancy.

        :param request: Request
        :return: Vacancy
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Delete the vacancy.

        :param request: Request
        :return: No Content
        """
        return self.destroy(request, *args, **kwargs)


class VacancyResponse(GenericAPIView):
    """Vacancy favorite view."""

    serializer_class = VacancySerializer
    queryset = Vacancy.objects.all()
    permission_classes: tuple = (
        IsAuthenticated,
        VacancyRespondedPermission,
        VacancyResponsePermission,
    )

    def get_queryset(self) -> QuerySet:
        """
        Get queryset.

        :return:
        """
        queryset = super().get_queryset()
        return queryset.filter(deleted_at__isnull=True)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get users who have responded to the vacancy.

        :param request: Request
        :return: List responded users
        """
        vacancy = self.get_object()
        serializer = UserSerializer(instance=vacancy.responded_users.all(),
                                    many=True,
                                    context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Apply for job.

        :param request: Request
        :return: Vacancy
        """
        serializer = self.get_serializer(self.get_object())
        serializer.add_response(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Remove vacancy response.

        :param request: Request
        :return: Vacancy
        """
        serializer = self.get_serializer(self.get_object())
        serializer.remove_response(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class VacancyTop(GenericAPIView):
    """Vacancy top view."""

    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes: tuple = (IsAuthenticated, VacancyTopPermission)

    def get_queryset(self) -> QuerySet:
        """
        Get queryset.

        :return:
        """
        queryset = super().get_queryset()
        return queryset.filter(deleted_at__isnull=True)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Set the vacancy as top.

        :param request: Request
        :return: Review instance
        """
        vacancy: Vacancy = self.get_object()
        if vacancy.company.vacancies.filter(deleted_at__isnull=True,
                                            is_top=True).count() >= 2:
            raise MaxTopVacancies
        vacancy.is_top = True
        vacancy.save()
        serializer = self.serializer_class(instance=vacancy,
                                           context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Unset the vacancy as favorite.

        :param request: Request
        :return: Review instance
        """
        vacancy: Vacancy = self.get_object()
        vacancy.is_top = False
        vacancy.save()
        serializer = self.serializer_class(instance=vacancy,
                                           context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
