"""Interview serializers."""
from rest_framework import serializers

from jobadvisor.common.validators import past_date
from jobadvisor.companies.serializers import (
    CompanySerializer,
    PositionSerializer,
)
from jobadvisor.reviews.models import Interview
from jobadvisor.reviews.serializers import CommentSerializer
from jobadvisor.reviews.serializers.qa import QASerializer
from jobadvisor.users.serializers import UserSerializer


class InterviewSerializer(serializers.ModelSerializer):
    """Interview serializer."""

    class Meta:
        """Meta."""

        model = Interview
        fields: list = [
            "id",
            "company",
            "owner",
            "position",
            "title",
            "description",
            "experience",
            "complication",
            "has_offer",
            "duration",
            "date",
            "place",
            "is_anonymous",
            "is_top",
            "created_at",
            "is_helpful",
            "has_report",
            "comments",
            "qas",
        ]
        read_only_fields: tuple = (
            "owner",
            "is_top",
            "created_at",
            "is_helpful",
            "has_report",
        )
        extra_kwargs: dict = {
            "date": {
                "validators": [past_date]
            },
        }

    comments = CommentSerializer(many=True, read_only=True)
    qas = QASerializer(many=True, read_only=True)
    is_helpful = serializers.SerializerMethodField()

    def to_representation(self, instance):
        """
        Anonymize user.

        :param instance:
        :return:
        """
        if instance.is_anonymous:
            instance.owner = None
        self.fields["company"] = CompanySerializer()
        self.fields["owner"] = UserSerializer(allow_null=True)
        self.fields["position"] = PositionSerializer()
        return super().to_representation(instance)

    def get_is_helpful(self, obj: Interview) -> dict:
        """
        Get helpful info.

        :param obj: Interview
        :return:
        """
        user = self.context["request"].user
        return {
            "to_me": obj.helpful.filter(id=user.pk).exists(),
            "count": obj.helpful.count(),
        }
