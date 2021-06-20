"""FAQ serializers."""
from rest_framework import serializers

from jobadvisor.landing.models import FAQ, Category


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""

    class Meta:
        """Meta."""

        model = Category
        fields: list = [
            "id",
            "name",
        ]


class FAQSerializer(serializers.ModelSerializer):
    """FAQ serializer."""

    class Meta:
        """Meta."""

        model = FAQ
        fields: list = [
            "id",
            "category",
            "level",
            "question",
            "answer",
        ]
