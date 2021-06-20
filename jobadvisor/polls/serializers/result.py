"""Result serializer."""
from rest_framework import serializers

from jobadvisor.polls.serializers import CategorySerializer


class ResultSerializer(serializers.Serializer):
    """Result serializer."""

    category = CategorySerializer()
    result = serializers.FloatField()
