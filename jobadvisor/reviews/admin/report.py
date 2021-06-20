"""Report admin."""
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.http import HttpRequest

from jobadvisor.reviews.models import Report


class ReportInline(GenericStackedInline):
    """Comment inline admin."""

    extra = 0
    model = Report
    fields: tuple = ("owner", "owner_email", "status", "text")
    readonly_fields: tuple = (
        "owner",
        "owner_email",
        "text",
    )

    def has_add_permission(self, request, obj=None):
        """
        Check add permission.

        :param request:
        :param obj:
        :return: False
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Check delete permission.

        :param request:
        :param obj:
        :return: False
        """
        return False

    @staticmethod
    def owner_email(obj: Report) -> str:
        """
        Get email owner this report.

        :return: Email
        """
        return str(obj.owner.email)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Report admin."""

    model = Report
    list_display: tuple = ("id", "owner", "status")
    list_display_links: tuple = list_display
    list_filter: tuple = ("status",)
    search_fields: tuple = (
        "owner__first_name",
        "owner__last_name",
        "text",
    )
    ordering: tuple = ("id",)
    fields: tuple = ("owner", "text", "status")
    readonly_fields: tuple = (
        "owner",
        "text",
    )
    can_delete: bool = False

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Check change permission.

        :param request:
        :return: False
        """
        return False
