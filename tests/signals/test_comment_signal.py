import pytest
from fcm_django.models import FCMDeviceQuerySet
from tests.factories import CommentedInterviewFactory


@pytest.mark.django_db
def test_comment_signal_create_subscription(mocker, review) -> None:
    mocker.spy(FCMDeviceQuerySet, "send_message")
    CommentedInterviewFactory(content_object=review)
    assert FCMDeviceQuerySet.send_message.call_count == 1
