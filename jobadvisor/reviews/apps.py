"""Reviews apps."""
from importlib import import_module

from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Reviews config."""

    name: str = "jobadvisor.reviews"

    def ready(self) -> None:
        """
        Ready app.

        :return: None
        """
        import_module("jobadvisor.reviews.signals")
