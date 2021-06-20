"""Categories views."""

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.polls.models import Category
from jobadvisor.polls.serializers import CategorySerializer


class CategoryList(GenericAPIView, ListModelMixin):
    """Category list view."""

    serializer_class = CategorySerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get category list.

        :param request: Request
        :return: List of category
        """
        return self.list(request, *args, **kwargs)


class CategoryDetail(GenericAPIView, RetrieveModelMixin):
    """Category detail view."""

    serializer_class = CategorySerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the category.

        :param request: Request
        :return: Category
        """
        return self.retrieve(request, *args, **kwargs)
