"""Industry views."""

from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.companies.models import Industry
from jobadvisor.companies.serializers import IndustrySerializer


class IndustryList(GenericAPIView, ListModelMixin):
    """Industry list view."""

    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    filter_backends: tuple = (SearchFilter,)
    search_fields: tuple = ("name",)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get industry list.

        :param request: Request
        :return: List of position
        """
        return self.list(request, *args, **kwargs)
