"""Position admin."""
from django.contrib import admin

from jobadvisor.companies.models import Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Position admin."""

    model = Position
    list_display: tuple = ("id", "name")
    search_fields: tuple = ("id", "name")
    ordering: tuple = ("id", "name")
