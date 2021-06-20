"""Variants views."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.polls.models import Variant
from jobadvisor.polls.serializers import VariantSerializer


class VariantList(GenericAPIView, ListModelMixin):
    """Variant list view."""

    serializer_class = VariantSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    queryset = Variant.objects.all()
    filter_backends: tuple = (DjangoFilterBackend,)
    filterset_fields: tuple = (
        "question",
    )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get variant list.

        :param request: Request
        :return: List of variant
        """
        return self.list(request, *args, **kwargs)


class VariantDetail(GenericAPIView, RetrieveModelMixin):
    """Variant detail view."""

    serializer_class = VariantSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    queryset = Variant.objects.all()

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the variant.

        :param request: Request
        :return: Variant item
        """
        return self.retrieve(request, *args, **kwargs)
