"""Notifications admin."""
from django.contrib import admin

from jobadvisor.notifications.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Message admin."""

    model = Message
    list_display: tuple = ("id", "owner")
    list_display_links: tuple = list_display
    search_fields: tuple = ("id", "text", "owner__last_name", "owner__first_name")
    ordering: tuple = ("id", "is_read")
    list_filter: tuple = ("is_read", "level")
    readonly_fields: tuple = ("is_read",)
    autocomplete_fields: tuple = ("owner",)
