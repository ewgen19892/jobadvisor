import pytest
from rest_framework.request import Request
from rest_framework.test import force_authenticate
from tests.factories import ReviewFactory

from jobadvisor.reviews.filters import ReviewFilter
from jobadvisor.reviews.models import Review


@pytest.mark.django_db
def test_review_filter_company(rf, reviews, review, employee):
    queryset = Review.objects.all()
    filterset = ReviewFilter()
    filtered_reviews = filterset._company(queryset, "company", review.company.pk)
    assert review in filtered_reviews
    assert all([r.company.pk == review.company.pk for r in filtered_reviews])


@pytest.mark.django_db
def test_review_filter_is_mine_true(rf, reviews, employee):
    review = ReviewFactory(owner=employee)
    queryset = Review.objects.all()
    request = rf.get("")
    force_authenticate(request, user=employee)
    filterset = ReviewFilter(request=Request(request))
    filtered_reviews = filterset._is_mine(queryset, "is_mine", True)
    assert review in filtered_reviews
    assert all([r.owner == employee for r in filtered_reviews])


@pytest.mark.django_db
def test_review_filter_is_mine_false(rf, reviews, employee):
    review = ReviewFactory(owner=employee)
    queryset = Review.objects.all()
    request = rf.get("")
    force_authenticate(request, user=employee)
    filterset = ReviewFilter(request=Request(request))
    filtered_reviews = filterset._is_mine(queryset, "is_mine", False)
    assert review not in filtered_reviews
    assert all([not r.owner == employee for r in filtered_reviews])
