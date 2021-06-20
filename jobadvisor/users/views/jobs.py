"""Jobs views."""
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
from jobadvisor.users.models import Job
from jobadvisor.users.serializers import JobSerializer


class JobList(GenericAPIView, CreateModelMixin, ListModelMixin):
    """Job list view."""

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    filter_backends: tuple = (DjangoFilterBackend,)
    filterset_fields: tuple = (
        "owner",
    )

    def perform_create(self, serializer: JobSerializer) -> None:
        """
        Perform create job.

        :param serializer:
        :return: None
        """
        serializer.save(owner=self.request.user)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get job list.

        :param request: Request
        :return: List of jobs
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create job item.

        :param request:
        :return: New job
        """
        return self.create(request, *args, **kwargs)


class JobDetail(GenericAPIView,
                RetrieveModelMixin,
                UpdateModelMixin,
                DestroyModelMixin):
    """Job detail view."""

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, OwnerPermission,)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the job.

        :param request: Request
        :return: Job
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Partial update the job.

        :param request: Request
        :return: Updated job
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Delete the job.

        :param request: Request
        :return: None
        """
        return self.destroy(request, *args, **kwargs)
