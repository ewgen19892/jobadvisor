"""Answers views."""
from django_filters.rest_framework import DjangoFilterBackend
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

from jobadvisor.common.permissions import OwnerPermission
from jobadvisor.polls.filters import AnswerFilter
from jobadvisor.polls.models import Answer
from jobadvisor.polls.serializers import AnswerSerializer


class AnswerList(GenericAPIView, CreateModelMixin, ListModelMixin):
    """Answer list view."""

    model = Answer
    queryset = Answer.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    serializer_class = AnswerSerializer
    filter_backends: tuple = (
        DjangoFilterBackend,
    )
    filterset_class = AnswerFilter

    def perform_create(self, serializer: AnswerSerializer) -> None:
        """
        Perform create answer.

        :param serializer:
        :return: None
        """
        serializer.save(owner=self.request.user)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get answer list.

        :param request: Request
        :return: Answer list
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create answer item.

        :param request: Request
        :return: New answer item
        """
        return self.create(request, *args, **kwargs)


class AnswerDetail(GenericAPIView,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin):
    """Answer detail view."""

    model = Answer
    queryset = Answer.objects.all()
    permission_classes: tuple = (OwnerPermission, IsAuthenticatedOrReadOnly)
    serializer_class = AnswerSerializer

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the answer.

        :param request: Request
        :return: Answer
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Partial update the answer.

        :param request: Request
        :return: Updated answer
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Delete the answer.

        :param request: Request
        :return: No Content
        """
        return self.destroy(request, *args, **kwargs)
