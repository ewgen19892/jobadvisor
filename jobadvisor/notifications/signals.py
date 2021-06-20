"""Notification signals."""
from django.db.models.signals import post_save
from django.dispatch import receiver

from jobadvisor.notifications.models import Message


@receiver(post_save, sender=Message)
def message_save(instance: Message, **kwargs: dict) -> None:
    """
    Send FCM notification after create message.

    :type instance: Message
    :return: None
    """
    if kwargs["created"]:
        instance.send()
