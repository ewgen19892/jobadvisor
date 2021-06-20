"""Registration views."""
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.users.models import User
from jobadvisor.users.serializers import UserSerializer
from jobadvisor.users.serializers.users import InviteSerializer


class UserRegistration(GenericAPIView, CreateModelMixin):
    """User registration view."""

    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes: tuple = (AllowAny,)

    def perform_create(self, serializer: UserSerializer) -> None:
        """
        Save serializer.

        :param serializer: Validated user serializer.
        :return: None
        """
        serializer.save(is_active=False)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Register user with credentials.

        :param request:
        :return:
        """
        return self.create(request, *args, **kwargs)


class UserInvite(GenericAPIView, CreateModelMixin):
    """Invite view."""

    queryset = User.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    serializer_class = InviteSerializer

    def post(self, request: Request) -> Response:
        """
        Invite user to JobAdvisor.

        :param request:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_serializer = UserSerializer(instance=serializer.instance)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class UserActivation(GenericAPIView):
    """User activate view."""

    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes: tuple = (AllowAny,)
    lookup_field = "uid"

    def get_object(self) -> User:
        """
        Get user by uid and check permissions.

        :return: User.
        """
        queryset = self.filter_queryset(self.get_queryset())
        uid = force_text(urlsafe_base64_decode(self.kwargs["uid"]))
        token = self.kwargs["token"]
        obj = get_object_or_404(queryset, pk=uid)
        self.check_object_permissions(self.request, obj)
        if not default_token_generator.check_token(user=obj, token=token):
            raise ParseError(_("Invalid token"))
        return obj

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Activate user.

        :param request:
        :return:
        """
        user = self.get_object()
        user.activate()
        serializer = self.get_serializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserRestore(GenericAPIView, UpdateModelMixin):
    """Restore user access."""

    queryset = User.objects.all()
    permission_classes: tuple = (AllowAny,)
    serializer_class = UserSerializer

    def get_object(self) -> User:
        """
        Get user by uid and check permissions.

        :return: User.
        """
        queryset = self.filter_queryset(self.get_queryset())
        uid = force_text(urlsafe_base64_decode(self.kwargs["uid"]))
        token = self.kwargs["token"]
        obj = get_object_or_404(queryset, pk=uid)
        self.check_object_permissions(self.request, obj)
        if not default_token_generator.check_token(user=obj, token=token):
            raise ParseError({"token": [_("Invalid token")]})
        return obj

    def perform_update(self, serializer: UserSerializer) -> None:
        """
        Save serializer.

        :param serializer: Validated user serializer.
        :return: None
        """
        serializer.save(is_active=True)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Request password restore.

        :return:
        """
        email = request.query_params.get("email", None)
        if email is None:
            raise ParseError({"email": [_("This parameter is required.")]})
        user = get_object_or_404(User, email=email)
        user.restore_password()
        serializer = self.get_serializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Restore user password.

        :param request:
        :return:
        """
        return self.partial_update(request, *args, **kwargs)
