"""Page admin."""
from django.contrib import admin

from jobadvisor.landing.models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """Category admin."""

    model = Page
    list_display: tuple = ("title",)
    list_display_links: tuple = list_display
    search_fields: tuple = ("title", "text")
    prepopulated_fields: dict = {"slug": ("title",)}
