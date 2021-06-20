"""Notifications models."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from fcm_django.models import FCMDevice


class MessageManager(models.Manager):
    """Message manager."""

    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        """Bulk create messages and send notifications."""
        messages = super().bulk_create(objs, batch_size, ignore_conflicts)
        _ = [message.send() for message in messages]
        return messages


class Message(models.Model):
    """Message model."""

    WARNING: str = "warning"
    INFO: str = "info"
    MESSAGE: str = "message"
    SUCCESS: str = "success"
    ALARM: str = "alarm"

    LEVELS: tuple = (
        (WARNING, _("Warning")),
        (INFO, _("Info")),
        (SUCCESS, _("Success")),
        (ALARM, _("Alarm")),
    )

    owner = models.ForeignKey(
        verbose_name=_("Owner"),
        to="users.User",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    level = models.CharField(
        verbose_name=_("Level"),
        max_length=12,
        choices=LEVELS,
    )
    text = models.TextField(verbose_name=_("Text"))
    is_read = models.BooleanField(
        verbose_name=_("Is read"),
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )

    objects: MessageManager = MessageManager()

    def __str__(self) -> str:
        """
        Call as string.

        :return: self text
        """
        return self.text

    def send(self) -> None:
        """Send message to owner with FCM."""
        devices = FCMDevice.objects.filter(user=self.owner).all()
        data = {
            "id": self.id,
            "owner": self.owner.id,
            "text": self.text,
            "level": self.level,
            "is_read": self.is_read,
            "created_at": str(self.created_at.isoformat()),
        }
        devices.send_message(data=data)
