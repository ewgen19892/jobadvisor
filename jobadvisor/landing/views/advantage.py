"""Advantage views."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.landing.models import Advantage
from jobadvisor.landing.serializers import AdvantageSerializer


class AdvantageList(GenericAPIView, ListModelMixin):
    """Advantage list view."""

    model: Advantage = Advantage
    queryset = Advantage.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    serializer_class = AdvantageSerializer
    filter_backends: tuple = (DjangoFilterBackend,)
    filterset_fields: tuple = (
        "level",
    )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get advantage list.

        :param request: Request
        :return: Advantage list
        """
        return self.list(request, *args, **kwargs)
