"""Industry admin."""
from django.contrib import admin

from jobadvisor.companies.models import Industry


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    """Industry admin."""

    model = Industry
    list_display: tuple = ("id", "name")
    search_fields: tuple = ("id", "name")
    ordering: tuple = ("id", "name")
