"""Position views."""

from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.companies.models import Position
from jobadvisor.companies.serializers import PositionSerializer


class PositionList(GenericAPIView, ListModelMixin, CreateModelMixin):
    """Position list view."""

    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    filter_backends: tuple = (SearchFilter,)
    search_fields: tuple = ("name",)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get position list.

        :param request: Request
        :return: List of positions
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create position.

        :param request:
        :return: New position
        """
        return self.create(request, *args, **kwargs)
