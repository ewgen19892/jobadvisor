"""Users views."""
from django.shortcuts import get_object_or_404

from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.users.models import User
from jobadvisor.users.permissions import UserPermission
from jobadvisor.users.serializers import UserSerializer


class UserList(GenericAPIView, ListModelMixin):
    """User list view."""

    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, UserPermission)
    filter_backends: tuple = (
        SearchFilter,
    )
    search_fields: tuple = ("email", "first_name", "last_name")

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get users list.

        :param request: Request
        :return: List of user
        """
        return self.list(request, *args, **kwargs)


class UserDetail(GenericAPIView, RetrieveModelMixin, UpdateModelMixin,
                 DestroyModelMixin):
    """User detail view."""

    model_class = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, UserPermission,)

    def get_object(self) -> User:
        """
        Get user object.

        :return: User instance.
        """
        if self.kwargs.get("pk") == "me":
            pk = self.request.user.pk
        else:
            pk = self.kwargs.get("pk")
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request=self.request, obj=user)
        return user

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the user.

        :param request: Request
        :return: Response
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Partial update the user.

        :param request: Request
        :return: Response
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Delete the user.

        :param request:
        :return:
        """
        return self.destroy(request, *args, **kwargs)
