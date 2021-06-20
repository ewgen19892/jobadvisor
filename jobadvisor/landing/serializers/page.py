"""Page serializers."""
from rest_framework import serializers

from jobadvisor.landing.models import Page


class PageSerializer(serializers.ModelSerializer):
    """Page serializer."""

    class Meta:
        """Meta."""

        model = Page
        fields: list = [
            "id",
            "title",
            "slug",
            "text",
        ]
