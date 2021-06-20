"""Page views."""
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.landing.models import Page
from jobadvisor.landing.serializers import PageSerializer


class PageList(GenericAPIView, ListModelMixin):
    """Page list view."""

    model: Page = Page
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get page list.

        :param request: Request
        :return: Page list
        """
        return self.list(request, *args, **kwargs)


class PageDetail(GenericAPIView, RetrieveModelMixin):
    """Page detail view."""

    model: Page = Page
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_field = "slug"

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the page.

        :param request: Request
        :return: Page
        """
        return self.retrieve(request, *args, **kwargs)
