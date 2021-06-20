"""Educations serializers."""
from rest_framework import serializers

from jobadvisor.users.models import Education
from jobadvisor.users.serializers.institute import InstituteSerializer


class EducationSerializer(serializers.ModelSerializer):
    """Education serializer."""

    class Meta:
        """Meta."""

        model = Education
        fields: list = [
            "id",
            "graduated",
            "speciality",
            "owner",
            "institute",
        ]
        extra_kwargs: dict = {
            "owner": {
                "read_only": True,
            },
        }

    def to_representation(self, instance: Education) -> dict:
        """
        Transform object.

        :param instance: Education
        :return: OrderedDict
        """
        self.fields["institute"] = InstituteSerializer()
        return super().to_representation(instance)
