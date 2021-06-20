"""Institute views."""
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.users.models import Institute
from jobadvisor.users.serializers import InstituteSerializer


class InstituteList(GenericAPIView, CreateModelMixin, ListModelMixin):
    """Institute list view."""

    model = Institute
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    filter_backends: tuple = (SearchFilter,)
    search_fields: tuple = ("name",)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get institute list.

        :param request: Request
        :return: List of institutions
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create institute.

        :param request:
        :return: New institute
        """
        return self.create(request, *args, **kwargs)
