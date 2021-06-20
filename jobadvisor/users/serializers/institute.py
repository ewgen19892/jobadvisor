"""Institute serializers."""
from rest_framework import serializers

from jobadvisor.users.models import Institute


class InstituteSerializer(serializers.ModelSerializer):
    """Institute serializer."""

    class Meta:
        """Meta."""

        model = Institute
        fields: list = [
            "id",
            "name",
        ]
