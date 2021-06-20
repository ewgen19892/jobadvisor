import pytest
from fcm_django.models import FCMDeviceQuerySet

from jobadvisor.common import notifications


@pytest.mark.django_db
def test_notification_success(mocker, employee) -> None:
    mocker.spy(FCMDeviceQuerySet, "send_message")
    notifications.fcm_notification([employee], notifications.INFO, "TEXT")
    assert FCMDeviceQuerySet.send_message.call_count == 1


def test_notification_bad_type() -> None:
    with pytest.raises(ValueError):
        notifications.fcm_notification([], "INFO", "TEXT")
