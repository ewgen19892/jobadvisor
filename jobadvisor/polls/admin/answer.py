"""Answer admin."""
from django.contrib import admin
from django.http import HttpRequest

from jobadvisor.polls.models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Answer admin."""

    model = Answer
    list_display: tuple = ("id", "owner", "company", "weight")
    list_display_links: tuple = list_display
    search_fields: tuple = (
        "id",
        "company__name",
        "owner__first_name",
        "owner__last_name",
    )

    readonly_fields: tuple = (
        "owner",
        "company",
        "question",
        "variant",
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Check add permission.

        :param request:
        :return: False
        """
        return False
