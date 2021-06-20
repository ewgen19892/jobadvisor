"""User job."""
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from jobadvisor.common.validators import past_date
from jobadvisor.companies.serializers.company import CompanySerializer
from jobadvisor.companies.serializers.position import PositionSerializer
from jobadvisor.users.models import Job
from jobadvisor.users.serializers.users import UserSerializer


class JobSerializer(serializers.ModelSerializer):
    """Job serializer."""

    class Meta:
        """Meta."""

        model = Job
        fields: list = [
            "id",
            "owner",
            "company",
            "position",
            "level",
            "salary",
            "started_at",
            "finished_at",
        ]
        extra_kwargs: dict = {
            "owner": {
                "read_only": True,
            },
            "started_at": {
                "validators": [past_date]
            },
            "finished_at": {
                "validators": [past_date]
            },
        }

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

    def to_representation(self, instance: Job) -> dict:
        """
        Transform object.

        :param instance: Resume
        :return: OrderedDict
        """
        self.fields["owner"] = UserSerializer()
        self.fields["position"] = PositionSerializer()
        self.fields["company"] = CompanySerializer()
        request = self.context.get("request")
        if not request or not request.user == instance.owner:
            instance.salary = None
        return super().to_representation(instance)
