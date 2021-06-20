"""Advantage serializers."""
from rest_framework import serializers

from jobadvisor.landing.models import Advantage


class AdvantageSerializer(serializers.ModelSerializer):
    """Advantage serializer."""

    class Meta:
        """Meta."""

        model = Advantage
        fields: list = [
            "id",
            "name",
            "file",
            "level",
        ]
        read_only_fields: tuple = fields
