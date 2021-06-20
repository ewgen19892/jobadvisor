"""Resumes serializers."""
from os.path import splitext

from rest_framework import serializers

from jobadvisor.companies.serializers.position import PositionSerializer
from jobadvisor.users.models import Resume
from jobadvisor.users.serializers.skill import SkillSerializer
from jobadvisor.users.serializers.users import UserSerializer


class ResumeSerializer(serializers.ModelSerializer):
    """Resume serializer."""

    @staticmethod
    def validate_file(file):
        """Validate file extension.

        :param file:
        :return:
        """
        if file:
            extension = splitext(file.name)[1]
            if extension not in (".pdf", ".doc", ".docx"):
                raise serializers.ValidationError("Only pdf, doc, docx files")
        return file

    def to_representation(self, instance: Resume) -> dict:
        """
        Transform object.

        :param instance: Resume
        :return: OrderedDict
        """
        self.fields["skills"] = SkillSerializer(many=True)
        self.fields["owner"] = UserSerializer()
        self.fields["position"] = PositionSerializer()
        return super().to_representation(instance)

    class Meta:
        """Meta."""

        model = Resume
        fields: list = [
            "id",
            "file",
            "position",
            "experience",
            "certificates",
            "description",
            "salary",
            "owner",
            "skills",
        ]
        extra_kwargs: dict = {
            "file": {
                "allow_null": True,
            },
            "certificates": {
                "allow_null": True,
            },
            "description": {
                "allow_null": True,
            },
            "skills": {
                "allow_empty": True,
            },
        }
