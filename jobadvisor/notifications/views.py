"""Notifications views."""
from django.db.models import QuerySet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.notifications.models import Message
from jobadvisor.notifications.serializers import MessageSerializer


class MessageList(GenericAPIView, ListModelMixin):
    """Message list view."""

    model: Message = Message
    queryset = Message.objects
    permission_classes: tuple = (IsAuthenticated,)
    filter_backends: tuple = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_fields: tuple = (
        "is_read",
    )
    ordering_fields: tuple = (
        "created_at",
        "level",
        "is_read",
    )
    serializer_class = MessageSerializer

    def get_queryset(self) -> QuerySet:
        """
        Get messages for authenticated user.

        :return: QuerySet
        """
        queryset = self.queryset.filter(owner=self.request.user)
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get message list.

        :param request: Request
        :return: Category list
        """
        return self.list(request, *args, **kwargs)


class MessageRead(GenericAPIView, RetrieveModelMixin):
    """Message list view."""

    model: Message = Message
    queryset = Message.objects
    permission_classes: tuple = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self) -> QuerySet:
        """
        Get messages for authenticated user.

        :return: QuerySet
        """
        queryset = self.queryset.filter(owner=self.request.user)
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def get_object(self) -> Message:
        """
        Get message by ID.

        :return: Message
        """
        message = super().get_object()
        if not message.is_read:
            message.is_read = True
            message.save()
        return message

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get message list.

        :param request: Request
        :return: Category list
        """
        return self.retrieve(request, *args, **kwargs)
