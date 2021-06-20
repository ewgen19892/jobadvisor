"""Review admin."""
from django.contrib import admin

from jobadvisor.reviews.admin.comment import CommentInline
from jobadvisor.reviews.admin.report import ReportInline
from jobadvisor.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review admin."""

    model = Review
    list_display: tuple = ("id", "company", "owner", "rate")
    list_display_links: tuple = list_display
    list_filter: tuple = ("is_anonymous",)
    search_fields: tuple = (
        "company__name",
        "owner__first_name",
        "owner__last_name",
        "title",
        "description",
    )
    ordering: tuple = ("id",)
    inlines: list = [CommentInline, ReportInline]

    fields = (
        "company",
        "owner",
        "title",
        "description",
        "rate",
        "improvements",
        "is_anonymous",
        "is_best",
    )
    readonly_fields: tuple = (
        "company",
        "owner",
        "title",
        "description",
        "rate",
        "improvements",
        "is_anonymous",
    )

    def has_add_permission(self, request):
        """
        Check add permission.

        :param request:
        :return: False
        """
        return False
