"""Report serializers."""
from rest_framework import serializers

from jobadvisor.reviews.models import Report


class ReportSerializer(serializers.ModelSerializer):
    """Report serializer."""

    class Meta:
        """Meta."""

        model = Report
        fields: list = [
            "id",
            "owner",
            "text",
            "status",
        ]
        extra_kwargs: dict = {
            "owner": {
                "read_only": True,
            },
            "status": {
                "read_only": True,
            },
        }
