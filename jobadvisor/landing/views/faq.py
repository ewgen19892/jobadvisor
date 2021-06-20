"""FAQ views."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.landing.models import FAQ, Category
from jobadvisor.landing.serializers import CategorySerializer, FAQSerializer


class CategoryList(GenericAPIView, ListModelMixin):
    """Category list view."""

    model: Category = Category
    queryset = Category.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    serializer_class = CategorySerializer

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get category list.

        :param request: Request
        :return: Category list
        """
        return self.list(request, *args, **kwargs)


class FAQList(GenericAPIView, ListModelMixin):
    """FAQ list view."""

    queryset = FAQ.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    serializer_class = FAQSerializer
    filter_backends: tuple = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_fields: tuple = (
        "level",
        "category",
    )

    search_fields: tuple = ("question", "answer")

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get FAQ list.

        :param request: Request
        :return: FAQ list
        """
        return self.list(request, *args, **kwargs)


class FAQDetail(GenericAPIView, RetrieveModelMixin):
    """FAQ detail view."""

    model: FAQ = FAQ
    queryset = FAQ.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    serializer_class = FAQSerializer

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the FAQ.

        :param request: Request
        :return: Answer FAQ
        """
        return self.retrieve(request, *args, **kwargs)
