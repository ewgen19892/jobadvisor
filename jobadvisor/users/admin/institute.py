"""Institute admin."""
from django.contrib import admin

from jobadvisor.users.models import Institute


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    """Institute admin."""

    model = Institute
    list_display: tuple = ("id", "name")
    search_fields: tuple = ("id", "name")
    ordering: tuple = ("id", "name")
