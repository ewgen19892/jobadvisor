import pytest
from tests.factories import ReviewFactory

from jobadvisor.reviews.serializers import ReviewSerializer


@pytest.mark.django_db
def test_review_serializer_validate(rf, position, company) -> None:
    review_stub = ReviewFactory.stub(position=position, company=company)
    data = {
        "company": review_stub.company.pk,
        "title": review_stub.title,
        "description": review_stub.description,
        "rate": review_stub.rate,
        "improvements": review_stub.improvements,
        "is_anonymous": review_stub.is_anonymous,
        "position": review_stub.position.pk,
        "started_at": review_stub.finished_at,
        "finished_at": review_stub.started_at,
    }
    serializer = ReviewSerializer(data=data)
    assert not serializer.is_valid()
