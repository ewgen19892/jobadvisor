"""Education admin."""
from django.contrib import admin

from jobadvisor.common.admin import ReadOnlyMixin
from jobadvisor.users.models import Education


class EducationInline(ReadOnlyMixin, admin.TabularInline):
    """Education inline admin."""

    model = Education
