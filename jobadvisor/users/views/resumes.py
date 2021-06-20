"""Resume views."""
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
from jobadvisor.users.models import Resume
from jobadvisor.users.serializers import ResumeSerializer


class ResumeList(GenericAPIView, ListModelMixin, CreateModelMixin):
    """Resume list view."""

    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, OwnerPermission,)
    filter_backends: tuple = (DjangoFilterBackend,)
    filterset_fields: tuple = (
        "owner",
    )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get resume list.

        :param request: Request
        :return: List of resumes
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create resume.

        :param request: Request
        :return: Resume instance
        """
        request.data["owner"] = request.user.pk
        return self.create(request, *args, **kwargs)


class ResumeDetail(GenericAPIView,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin):
    """Resume detail view."""

    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, OwnerPermission,)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the resume.

        :param request: Request
        :return: Resume instance
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Partial update the resume.

        :param request: Request
        :return: Updated resume instance
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Delete the resume.

        :param request: Request
        :return: No content
        """
        return self.destroy(request, *args, **kwargs)
