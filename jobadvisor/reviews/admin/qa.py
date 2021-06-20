"""QA admin."""
from django.contrib import admin

from jobadvisor.common.admin import ReadOnlyMixin
from jobadvisor.reviews.models import QA


class QAInline(ReadOnlyMixin, admin.StackedInline):
    """QA inline admin."""

    model = QA
