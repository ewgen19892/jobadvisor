"""Notifications config."""
from importlib import import_module

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Notifications config."""

    name = "jobadvisor.notifications"

    def ready(self) -> None:
        """
        Ready app.

        :return: None
        """
        import_module("jobadvisor.notifications.signals")
