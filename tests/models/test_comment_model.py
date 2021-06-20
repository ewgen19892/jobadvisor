import pytest
from tests.factories import CommentedReviewFactory


@pytest.mark.django_db
def test_comment_name() -> None:
    comment = CommentedReviewFactory.build()
    assert str(comment) == f"Comment: {comment.pk}"
