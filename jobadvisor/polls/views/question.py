"""Questions views."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.polls.models import Question
from jobadvisor.polls.serializers import QuestionSerializer


class QuestionList(GenericAPIView, ListModelMixin):
    """Question list view."""

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    filter_backends: tuple = (DjangoFilterBackend,)
    filterset_fields: tuple = (
        "category",
    )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get question list.

        :param request: Request
        :return: List of question
        """
        return self.list(request, *args, **kwargs)


class QuestionDetail(GenericAPIView, RetrieveModelMixin):
    """Question detail view."""

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the question.

        :param request: Request
        :return: Question
        """
        return self.retrieve(request, *args, **kwargs)
