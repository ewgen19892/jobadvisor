"""Subscription serializers."""
from rest_framework import serializers

from jobadvisor.companies.models.subscription import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """Subscription serializer."""

    class Meta:
        """Meta."""

        model = Subscription
        fields: list = [
            "id",
            "company",
            "plan",
            "is_trial",
            "started_at",
            "finished_at",
        ]
