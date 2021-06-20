"""Job admin."""
from django.contrib import admin

from jobadvisor.common.admin import ReadOnlyMixin
from jobadvisor.users.models import Job


class JobInline(ReadOnlyMixin, admin.TabularInline):
    """Job inline admin."""

    model = Job
