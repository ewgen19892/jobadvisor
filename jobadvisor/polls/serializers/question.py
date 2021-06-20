"""Questions serializers."""
from rest_framework import serializers

from jobadvisor.polls.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer."""

    class Meta:
        """Meta."""

        model = Question
        fields: list = [
            "id",
            "text",
            "category",
        ]
