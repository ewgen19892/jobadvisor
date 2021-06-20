"""Users admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from fcm_django.models import FCMDevice

from jobadvisor.users.models import User

from .education import EducationInline
from .job import JobInline
from .resume import ResumeInline


class DeviceInline(admin.TabularInline):
    """Resume inline admin."""

    model = FCMDevice
    fields: tuple = ("device_id", "type", "active")
    readonly_fields = fields
    extra: int = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin, admin.ModelAdmin):
    """User admin."""

    model = User
    inlines: list = [EducationInline, JobInline, ResumeInline, DeviceInline]
    list_display: tuple = ("id", "first_name", "last_name", "last_level")
    list_display_links: tuple = list_display
    list_filter: tuple = ("level", "is_staff", "is_banned")
    search_fields: tuple = ("first_name", "last_name", "email", "phone")
    ordering: tuple = ("pk",)
    fieldsets = (
        (_("Personal info"), {"fields": (
            "first_name",
            "last_name",
            "email",
            "phone",
            "level",
            "last_salary",
            "last_level",
        )}
         ),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_banned")}
         ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields: tuple = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "level",
        "last_login",
        "date_joined",
        "date_joined",
        "last_salary",
        "last_level",
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Check add permission.

        :param request:
        :return: False
        """
        return False

    @staticmethod
    def last_salary(obj: User) -> int:
        """
        Get user salary.

        :return: Salary from last job
        """
        return obj.jobs.values_list("salary", flat=True).last()

    last_salary.short_description = _("Last salary")  # noqa

    @staticmethod
    def last_level(obj: User) -> str:
        """
        Get user level.

        :return: Level from last job
        """
        last_job = obj.jobs.last()
        return last_job.get_level_display() if last_job else None

    last_level.short_description = _("Last job level")  # noqa
