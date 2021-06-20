"""Position serializers."""
from rest_framework import serializers

from jobadvisor.companies.models.position import Position


class PositionSerializer(serializers.ModelSerializer):
    """Position serializer."""

    class Meta:
        """Meta."""

        model = Position
        fields: list = [
            "id",
            "name",
        ]
