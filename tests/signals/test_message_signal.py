import pytest
from fcm_django.models import FCMDeviceQuerySet
from tests.factories import MessageFactory


@pytest.mark.django_db
def test_message_signal_save(mocker, review) -> None:
    mocker.patch.object(FCMDeviceQuerySet, "send_message")
    MessageFactory()
    assert FCMDeviceQuerySet.send_message.call_count == 1
