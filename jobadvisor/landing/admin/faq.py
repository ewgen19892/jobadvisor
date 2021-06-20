"""Category admin."""
from django.contrib import admin

from jobadvisor.landing.models import FAQ, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin."""

    model = Category
    list_display: tuple = ("id", "name")
    list_display_links: tuple = list_display
    search_fields: tuple = ("id", "name")
    ordering: tuple = ("id", "name")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """FAQ admin."""

    model = FAQ
    list_display: tuple = ("question", "category", "level")
    list_display_links: tuple = list_display
    search_fields: tuple = ("category__name", "question")
    ordering: tuple = ("id", "category")
    list_filter: tuple = ("category",)
