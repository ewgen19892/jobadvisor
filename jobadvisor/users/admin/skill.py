"""Skill admin."""
from django.contrib import admin

from jobadvisor.users.models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Skill admin."""

    model = Skill
    list_display: tuple = ("id", "name")
    search_fields: tuple = ("id", "name")
    ordering: tuple = ("id", "name")
