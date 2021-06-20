"""Notifications serializers."""
from rest_framework import serializers

from jobadvisor.notifications.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Message serializer."""

    class Meta:
        """Meta."""

        model = Message
        fields: list = [
            "id",
            "owner",
            "text",
            "level",
            "is_read",
            "created_at",
        ]
