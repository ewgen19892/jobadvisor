"""Interview admin."""
from django.contrib import admin

from jobadvisor.reviews.admin.comment import CommentInline
from jobadvisor.reviews.admin.qa import QAInline
from jobadvisor.reviews.admin.report import ReportInline
from jobadvisor.reviews.models import Interview


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    """Interview admin."""

    model = Interview
    list_display: tuple = ("id", "company", "owner", "experience")
    list_display_links: tuple = list_display
    list_filter: tuple = ("is_anonymous", "experience")
    search_fields: tuple = (
        "company__name",
        "owner__first_name",
        "owner__last_name",
        "title",
        "description",
    )
    ordering: tuple = ("id",)
    inlines: list = [QAInline, CommentInline, ReportInline]

    fields = (
        "company",
        "owner",
        "position",
        "title",
        "description",
        "experience",
        "complication",
        "has_offer",
        "duration",
        "date",
        "place",
        "is_anonymous",
    )
    readonly_fields: tuple = (
        "company",
        "owner",
        "position",
        "title",
        "description",
        "experience",
        "complication",
        "has_offer",
        "duration",
        "date",
        "place",
        "is_anonymous",
    )

    def has_add_permission(self, request):
        """
        Check add permission.

        :param request:
        :return: False
        """
        return False
