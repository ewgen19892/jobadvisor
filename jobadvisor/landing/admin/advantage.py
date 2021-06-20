"""Advantage admin."""
from django.contrib import admin

from jobadvisor.landing.models import Advantage


@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    """Advantage admin."""

    model = Advantage
    list_display: tuple = ("id", "name")
    list_display_links: tuple = list_display
    search_fields: tuple = ("id", "name")
    ordering: tuple = ("id", "name")
    readonly_fields: tuple = ("file_img",)
