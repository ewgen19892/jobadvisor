"""Comment views."""

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.reviews.models import Interview, Review
from jobadvisor.reviews.serializers import ReportSerializer


class ReportReview(GenericAPIView, CreateModelMixin):
    """Comment review view."""

    queryset = Review.objects.all()
    serializer_class = ReportSerializer
    permission_classes: tuple = (IsAuthenticated,)

    def perform_create(self, serializer: ReportSerializer) -> None:
        """
        Perform create a review report.

        :param serializer:
        :return: None
        """
        serializer.save(owner=self.request.user,
                        content_object=self.get_object())

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create the report.

        :param request: Request
        :return: New report instance
        """
        return self.create(request, *args, **kwargs)


class ReportInterview(GenericAPIView, CreateModelMixin):
    """Comment review view."""

    queryset = Interview.objects.all()
    serializer_class = ReportSerializer
    permission_classes: tuple = (IsAuthenticated,)

    def perform_create(self, serializer: ReportSerializer) -> None:
        """
        Perform create a interview report.

        :param serializer:
        :return: None
        """
        serializer.save(owner=self.request.user,
                        content_object=self.get_object())

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create the report.

        :param request: Request
        :return: New report instance
        """
        return self.create(request, *args, **kwargs)
