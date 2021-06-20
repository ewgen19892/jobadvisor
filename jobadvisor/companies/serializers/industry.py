"""Industry serializers."""
from rest_framework import serializers

from jobadvisor.companies.models import Industry


class IndustrySerializer(serializers.ModelSerializer):
    """Industry serializer."""

    class Meta:
        """Meta."""

        model = Industry
        fields: list = [
            "id",
            "name",
        ]
