"""Educations views."""
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
from jobadvisor.users.models import Education
from jobadvisor.users.serializers import EducationSerializer


class EducationList(GenericAPIView, CreateModelMixin, ListModelMixin):
    """Education list view."""

    model_class = Education
    serializer_class = EducationSerializer
    queryset = Education.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, OwnerPermission,)
    filter_backends: tuple = (DjangoFilterBackend,)
    filterset_fields: tuple = (
        "owner",
    )

    def perform_create(self, serializer: EducationSerializer) -> None:
        """
        Perform create education.

        :param serializer:
        :return: None
        """
        serializer.save(owner=self.request.user)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the education.

        :param request: Request
        :return: List of educations
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create the education.

        :param request: Request
        :return: New education
        """
        return self.create(request, *args, **kwargs)


class EducationDetail(GenericAPIView,
                      RetrieveModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin):
    """Education detail view."""

    model_class = Education
    serializer_class = EducationSerializer
    queryset = Education.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, OwnerPermission,)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the education.

        :param request: Request
        :return: Response
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Partial update the education.

        :param request: Request
        :return: Updated instance
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Delete the education.

        :param request: Request
        :return: Response
        """
        return self.destroy(request, *args, **kwargs)
