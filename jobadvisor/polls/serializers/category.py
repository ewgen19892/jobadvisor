"""Categories serializers."""
from rest_framework import serializers

from jobadvisor.polls.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""

    class Meta:
        """Meta."""

        model = Category
        fields: list = [
            "id",
            "name",
        ]
        ref_name: str = "Poll category"
