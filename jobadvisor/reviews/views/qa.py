"""QA views."""
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

from jobadvisor.reviews.models import QA
from jobadvisor.reviews.permissions import QAPermission
from jobadvisor.reviews.serializers import QASerializer


class QAList(GenericAPIView, CreateModelMixin, ListModelMixin):
    """QA list view."""

    queryset = QA.objects.all()
    serializer_class = QASerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, QAPermission)
    filter_backends: tuple = (DjangoFilterBackend,)
    filterset_fields: tuple = (
        "interview",
    )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get qa list.

        :param request: Request
        :return: QA list
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create the qa.

        :param request: Request
        :return: New qa instance
        """
        return self.create(request, *args, **kwargs)


class QADetail(GenericAPIView,
               RetrieveModelMixin,
               UpdateModelMixin,
               DestroyModelMixin):
    """QA detail view."""

    queryset = QA.objects.all()
    serializer_class = QASerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, QAPermission)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the qa.

        :param request: Request
        :return: QA instance
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Partial update the qa.

        :param request: Request
        :return: QA instance
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Delete the qa.

        :param request: Request
        :return: None
        """
        return self.destroy(request, *args, **kwargs)
