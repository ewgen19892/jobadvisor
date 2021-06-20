from django.urls import reverse

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from tests.factories import (
    CompanyFactory,
    ReviewFactory,
    SubscriptionFactory,
    UserFactory,
)

from jobadvisor.reviews.serializers import ReviewSerializer
from jobadvisor.reviews.views import ReviewDetail, ReviewHelpful, ReviewList


@pytest.mark.django_db
def test_reviews_list_success(rf, reviews):
    request = rf.get("")
    response = ReviewList.as_view()(request)
    assert int(response["X-Total"]) == len(reviews)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_review_create_success(rf, position, company):
    review_stub = ReviewFactory.stub(position=position, company=company)
    data = {
        "company": review_stub.company.pk,
        "title": review_stub.title,
        "description": review_stub.description,
        "rate": review_stub.rate,
        "improvements": review_stub.improvements,
        "is_anonymous": review_stub.is_anonymous,
        "position": review_stub.position.pk,
        "started_at": review_stub.started_at,
        "finished_at": review_stub.finished_at,
    }
    request = rf.post("", data=data)
    force_authenticate(request, user=UserFactory())
    response = ReviewList.as_view()(request)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_review_detail_success(rf, review, reviews):
    request = rf.get("")
    response = ReviewDetail.as_view()(request, pk=review.pk)
    review.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert ReviewSerializer(instance=review,
                            context={"request": request}).data == response.data


@pytest.mark.django_db
def test_review_update_success(rf, review):
    review_stub = ReviewFactory.stub(company=None, position=None)
    data = {
        "title": review_stub.title,
        "description": review_stub.description,
        "rate": review_stub.rate,
        "improvements": review_stub.improvements,
        "is_anonymous": True,
        "started_at": review_stub.started_at,
        "finished_at": review_stub.finished_at,
    }
    request = rf.patch("", data=data, content_type="application/json")
    force_authenticate(request, user=review.owner)
    response = ReviewDetail.as_view()(request, pk=review.pk)
    review.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert ReviewSerializer(instance=review,
                            context={"request": request}).data == response.data
    assert not response.data["owner"]


@pytest.mark.django_db
def test_review_delete_success(rf, review):
    request = rf.delete("")
    force_authenticate(request, user=review.owner)
    response = ReviewDetail.as_view()(request, pk=review.pk)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_review_helpful_add_success(rf, review):
    request = rf.post("")
    force_authenticate(request, user=UserFactory())
    response = ReviewHelpful.as_view()(request, pk=review.pk)
    assert response.data["is_helpful"]["to_me"]


@pytest.mark.django_db
def test_review_helpful_remove_success(rf, review):
    request = rf.delete("")
    force_authenticate(request, user=UserFactory())
    response = ReviewHelpful.as_view()(request, pk=review.pk)
    assert not response.data["is_helpful"]["to_me"]


class ReviewFavoriteTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory(owner=cls.user)
        cls.review = ReviewFactory(owner=cls.user,
                                   company=cls.company,
                                   is_top=False)
        cls.another_user = UserFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.subscription = SubscriptionFactory(company=self.company, plan=2)
        self.url = reverse("reviews:review_top",
                           kwargs={"pk": self.review.pk})

    def test_review_top_add_success(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_top"])

    def test_review_top_add_no_subscription(self):
        self.company.subscriptions.all().delete()
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_top_add_no_worker(self):
        self.client.force_authenticate(user=self.another_user)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_top_add_exceeded_limit(self):
        for _ in range(self.fake.random_int(min=10, max=15)):
            ReviewFactory(company=self.company, is_top=True)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_review_top_remove_success(self):
        self.review.is_top = True
        self.review.save()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_top"])
