"""Companies apps."""
from importlib import import_module

from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    """Companies config."""

    name: str = "jobadvisor.companies"

    def ready(self) -> None:
        """
        Ready app.

        :return: None
        """
        import_module("jobadvisor.companies.signals")
