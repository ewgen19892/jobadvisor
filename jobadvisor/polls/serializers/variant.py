"""Variants serializers."""
from rest_framework import serializers

from jobadvisor.polls.models import Variant


class VariantSerializer(serializers.ModelSerializer):
    """Variant serializer."""

    class Meta:
        """Meta."""

        model = Variant
        fields: list = [
            "id",
            "question",
            "is_positive",
            "weight",
            "text",
        ]
