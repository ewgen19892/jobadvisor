"""Skill views."""
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.users.models import Skill
from jobadvisor.users.serializers import SkillSerializer


class SkillList(GenericAPIView, CreateModelMixin, ListModelMixin):
    """Skill list view."""

    model = Skill
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    filter_backends: tuple = (SearchFilter,)
    search_fields: tuple = ("name",)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get skill list.

        :param request: Request
        :return: Response
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create skill.

        :param request:
        :return: New skill.
        """
        return self.create(request, *args, **kwargs)
