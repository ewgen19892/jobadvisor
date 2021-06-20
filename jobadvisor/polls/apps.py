"""Polls apps."""
from importlib import import_module

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Polls app config."""

    name: str = "jobadvisor.polls"

    def ready(self) -> None:
        """
        Ready app.

        :return: None
        """
        import_module("jobadvisor.polls.signals")
