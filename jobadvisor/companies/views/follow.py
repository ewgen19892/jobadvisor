"""Companies views."""
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.companies.models import Company
from jobadvisor.companies.permissions import CompanyFollowPermission
from jobadvisor.companies.serializers import FollowSerializer


class CompanyFollow(GenericAPIView, CreateModelMixin):
    """Company follow view."""

    serializer_class = FollowSerializer
    queryset = Company.objects.all()
    permission_classes: tuple = (
        IsAuthenticated,
        CompanyFollowPermission,
    )

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the company.

        :param request: Request
        :return: List of follows
        """
        queryset = self.filter_queryset(self.get_object().follows.all())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Add the company to favorites.

        :return: Follow instance
        """
        company = self.get_object()
        data = request.data.copy()
        data["company"] = company.pk
        data["owner"] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def delete(self,
               request: Request,
               *args: tuple,
               **kwargs: dict) -> Response:
        """
        Remove the company from favorites.

        :return: None
        """
        company = self.get_object()
        self.request.user.following.remove(company)
        return Response(status=status.HTTP_204_NO_CONTENT)
