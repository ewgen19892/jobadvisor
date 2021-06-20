"""Review views."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request
from rest_framework.response import Response

from jobadvisor.common.permissions import OwnerPermission
from jobadvisor.reviews.exceptions import MaxFavoriteReview
from jobadvisor.reviews.filters import ReviewFilter
from jobadvisor.reviews.models import Review
from jobadvisor.reviews.permissions import CompanyFavoritePermission
from jobadvisor.reviews.serializers import ReviewSerializer


class ReviewList(GenericAPIView, CreateModelMixin, ListModelMixin):
    """Review list view."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly,)
    filter_backends: tuple = (
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    )
    filterset_class = ReviewFilter
    search_fields: tuple = (
        "title",
        "description",
        "company__name",
    )
    ordering_fields: tuple = (
        "created_at",
        "rate",
    )

    def perform_create(self, serializer: ReviewSerializer) -> None:
        """
        Perform create review.

        :param serializer:
        :return: None
        """
        serializer.save(owner=self.request.user)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get review list.

        :param request: Request
        :return: List of reviews
        """
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Create the review.

        :param request: Request
        :return: New company
        """
        return self.create(request, *args, **kwargs)


class ReviewDetail(GenericAPIView,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin):
    """Review detail view."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes: tuple = (IsAuthenticatedOrReadOnly, OwnerPermission,)

    def get(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Get the review.

        :param request: Request
        :return: Review
        """
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Partial update the review.

        :param request: Request
        :return: Updated review
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Delete the company.

        :param request: Request
        :return: No Content
        """
        return self.destroy(request, *args, **kwargs)


class ReviewTop(GenericAPIView):
    """Review favorite view."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes: tuple = (IsAuthenticated, CompanyFavoritePermission)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Set the review as favorite.

        :param request: Request
        :return: Review instance
        """
        review: Review = self.get_object()
        if review.company.reviews.filter(is_top=True).count() >= 10:
            raise MaxFavoriteReview
        review.is_top = True
        review.save()
        serializer: ReviewSerializer = self.get_serializer(instance=review)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Unset the review as favorite.

        :param request: Request
        :return: Review instance
        """
        review: Review = self.get_object()
        review.is_top = False
        review.save()
        serializer: ReviewSerializer = self.get_serializer(review)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ReviewHelpful(GenericAPIView):
    """Review helpful view."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes: tuple = (IsAuthenticated,)

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Set the review as helpful.

        :param request: Request
        :return: Review
        """
        review: Review = self.get_object()
        review.helpful.add(request.user)
        serializer: ReviewSerializer = self.get_serializer(review)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, *args: tuple,
               **kwargs: dict) -> Response:
        """
        Unset the review as helpful.

        :param request: Request
        :return: Review
        """
        review: Review = self.get_object()
        review.helpful.remove(request.user)
        serializer: ReviewSerializer = self.get_serializer(review)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
