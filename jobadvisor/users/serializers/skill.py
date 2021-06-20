"""Skill serializers."""
from rest_framework import serializers

from jobadvisor.users.models import Skill


class SkillSerializer(serializers.ModelSerializer):
    """Skill serializer."""

    class Meta:
        """Meta."""

        model = Skill
        fields: list = [
            "id",
            "name",
        ]
