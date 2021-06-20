"""JobAdvisor notifications."""
from datetime import datetime

from fcm_django.models import FCMDevice

WARNING: str = "warning"
INFO: str = "info"
MESSAGE: str = "message"
SUCCESS: str = "success"
ALARM: str = "alarm"

NOTIFICATION_TYPES: tuple = (
    WARNING,
    INFO,
    MESSAGE,
    SUCCESS,
    ALARM,
)


def fcm_notification(users, notification_type, message) -> None:
    """
    Send FCM notification.

    :param message: Notification message
    :param users: User QuerySet
    :param notification_type: One of `NOTIFICATION_TYPES`
    :return: None
    """
    if notification_type not in NOTIFICATION_TYPES:
        raise ValueError(
            f"Notification type must be one of {NOTIFICATION_TYPES}")
    devices = FCMDevice.objects.filter(user__in=users).all()
    data: dict = {
        "type": notification_type,
        "message": message,
        "datetime": str(datetime.utcnow()),
    }
    devices.send_message(data=data)
