"""User favorites."""
from rest_framework import serializers

from jobadvisor.companies.models import Follow
from jobadvisor.users.serializers.users import UserSerializer


class FollowSerializer(serializers.ModelSerializer):
    """Follow serializer."""

    class Meta:
        """Meta."""

        model = Follow
        fields: list = [
            "id",
            "owner",
            "company",
            "description",
        ]

    def to_representation(self, instance):
        """
        Change representation view.

        :param instance:
        :return: Follow data
        """
        self.fields["owner"] = UserSerializer()
        return super().to_representation(instance)
