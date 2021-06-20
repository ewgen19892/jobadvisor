"""Salary serializers."""
from rest_framework import serializers


class SalarySerializer(serializers.Serializer):
    """Salary serializer."""

    position = serializers.CharField(source="name")
    max = serializers.FloatField()
    min = serializers.FloatField()
    avg = serializers.FloatField()
    count = serializers.IntegerField()
