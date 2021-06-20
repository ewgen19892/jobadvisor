"""Category admin."""
from django.contrib import admin

from jobadvisor.polls.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin."""

    model = Category
    list_display: tuple = ("id", "name")
    list_display_links: tuple = list_display
    search_fields: tuple = ("id", "name")
    ordering: tuple = ("id", "name")
