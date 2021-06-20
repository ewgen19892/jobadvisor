"""Review serializers."""
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from jobadvisor.common.validators import past_date
from jobadvisor.companies.serializers import (
    CompanySerializer,
    PositionSerializer,
)
from jobadvisor.reviews.models import Review
from jobadvisor.reviews.serializers import CommentSerializer
from jobadvisor.users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer."""

    class Meta:
        """Meta."""

        model = Review
        fields: list = [
            "id",
            "company",
            "owner",
            "title",
            "description",
            "rate",
            "improvements",
            "is_anonymous",
            "position",
            "started_at",
            "finished_at",
            "is_top",
            "is_best",
            "created_at",
            "is_helpful",
            "has_report",
            "comments",
        ]
        read_only_fields: tuple = (
            "owner",
            "is_top",
            "is_best",
            "created_at",
            "is_helpful",
            "has_report",
        )
        extra_kwargs: dict = {
            "position": {
                "allow_null": False,
                "required": True,
            },
            "started_at": {
                "allow_null": False,
                "required": True,
                "validators": [past_date]
            },
            "finished_at": {
                "validators": [past_date]
            },
        }

    comments = CommentSerializer(many=True, read_only=True)
    is_helpful = serializers.SerializerMethodField()

    def validate(self, attrs: dict) -> dict:
        """
        Validate data.

        :return: validated data.
        """
        attrs = super().validate(attrs)
        finished_at = attrs.get("finished_at")
        if finished_at and attrs.get("started_at") > finished_at:
            raise serializers.ValidationError(
                {"finished_at": _("started_at cannot be greater than finished_at")})
        return attrs

    def to_representation(self, instance):
        """
        Anonymize user.

        :param instance:
        :return:
        """
        if instance.is_anonymous:
            instance.owner = None
        self.fields["company"] = CompanySerializer()
        self.fields["owner"] = UserSerializer()
        self.fields["position"] = PositionSerializer()
        return super().to_representation(instance)

    def get_is_helpful(self, obj: Review) -> dict:
        """
        Get helpful info.

        :param obj: Interview
        :return:
        """
        helpful_to_me: bool = False
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            helpful_to_me = obj.helpful.filter(id=request.user.pk).exists()
        return {
            "to_me": helpful_to_me,
            "count": obj.helpful.count(),
        }
