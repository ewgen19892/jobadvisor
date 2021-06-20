from tests.factories import ReviewFactory


def test_review_name() -> None:
    review = ReviewFactory.build()
    assert str(review) == f"Review: {review.pk}"
