"""Question admin."""
from django.contrib import admin

from jobadvisor.polls.models import Question

from .variant import VariantInline


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Question admin."""

    model = Question
    inlines: list = [VariantInline]
    list_display: tuple = ("id", "text", "category")
    list_display_links: tuple = list_display
    search_fields: tuple = ("id", "text", "category__name")
    ordering: tuple = ("id", "text")
    list_filter: tuple = ("category",)
