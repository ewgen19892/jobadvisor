"""Resume admin."""
from django.contrib import admin

from jobadvisor.common.admin import ReadOnlyMixin
from jobadvisor.users.models import Resume


class ResumeInline(ReadOnlyMixin, admin.StackedInline):
    """Resume inline admin."""

    model = Resume
    readonly_fields: tuple = (
        "file",
        "position",
        "experience",
        "certificates",
        "description",
        "salary",
        "owner",
        "skills",
    )
