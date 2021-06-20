"""Interview views."""
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

from jobadvisor.common.permissions import OwnerPermission
from jobadvisor.reviews.exceptions import MaxFavoriteInterview
from jobadvisor.reviews.filters import InterviewFilter
from jobadvisor.reviews.models import Interview
from jobadvisor.reviews.permissions import CompanyFavoritePermission
from jobadvisor.reviews.serializers import InterviewSerializer


class InterviewList(GenericAPIView, CreateModelMixin, ListModelMixin):
    """Interview list view."""

    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    filter_backends: tuple = (
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    )
    filterset_class = InterviewFilter
    search_fields: tuple = (
        "title",
        "description",
        "place",
        "company__name",
        "position__name",
    )
    ordering_fields: tuple = (
        "created_at",
    )

    def perform_create(self, serializer: InterviewSerializer) -> None:
        """
        Perform create interview.

        :param serializer:
        :return: None
        """
        serializer.save(owner=self.request.user)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get interview list.

        :param request: Request
        :return: List of interviews
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create the interview.

        :param request: Request
        :return: New interview
        """
        return self.create(request, *args, **kwargs)


class InterviewDetail(GenericAPIView,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin):
    """Interview detail view."""

    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, OwnerPermission,)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the interview.

        :param request: Request
        :return: Interview
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Partial update the interview.

        :param request: Request
        :return: Updated interview
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Delete the interview.

        :param request: Request
        :return: No Content
        """
        return self.destroy(request, *args, **kwargs)


class InterviewTop(GenericAPIView):
    """Interview favorite view."""

    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes: tuple = (IsAuthenticated, CompanyFavoritePermission)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Set the interview as favorite.

        :param request: Request
        :return: Interview instance
        """
        interview: Interview = self.get_object()
        if interview.company.interviews.filter(is_top=True).count() >= 10:
            raise MaxFavoriteInterview
        interview.is_top = True
        interview.save()
        serializer: InterviewSerializer = self.get_serializer(interview)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Unset the interview as favorite.

        :param request: Request
        :return: Interview
        """
        interview: Interview = self.get_object()
        interview.is_top = False
        interview.save()
        serializer: InterviewSerializer = self.get_serializer(interview)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class InterviewHelpful(GenericAPIView):
    """Interview helpful view."""

    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes: tuple = (IsAuthenticated,)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Set the interview as helpful.

        :param request: Request
        :return: Interview
        """
        interview: Interview = self.get_object()
        interview.helpful.add(request.user)
        serializer: InterviewSerializer = self.get_serializer(interview)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Unset the interview as helpful.

        :param request: Request
        :return: Interview
        """
        interview: Interview = self.get_object()
        interview.helpful.remove(request.user)
        serializer: InterviewSerializer = self.get_serializer(interview)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
