"""QA serializers."""
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from jobadvisor.reviews.models import QA, Interview


class QASerializer(serializers.ModelSerializer):
    """QA serializer."""

    class Meta:
        """Meta."""

        model = QA
        fields: list = [
            "id",
            "interview",
            "question",
            "answer",
        ]

    def validate_interview(self, interview: Interview) -> Interview:
        """
        Validate interview.

        Check if the request user is the owner of this interview.
        :param interview:
        :return:
        """
        if interview and not interview.owner == self.context["request"].user:
            raise PermissionDenied()
        return interview
