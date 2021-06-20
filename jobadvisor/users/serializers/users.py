"""Users serializers."""
from typing import Dict

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from jobadvisor.users.models import User


class InviteSerializer(serializers.Serializer):
    """Invite serializer."""

    email: str = serializers.EmailField()

    def create(self, validated_data: dict) -> User:
        """
        Invite or get user.

        :param validated_data:
        :return: User
        """
        email = validated_data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.invite_user(email)
        return user


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    def validate_password(self, password: str) -> str:
        """
        Validate password.

        :param password:
        :return:
        """
        validate_password(password)
        if self.instance is None:
            return password
        return make_password(password)

    def create(self, validated_data: dict) -> User:
        """
        Create user.

        :param validated_data:
        :return:
        """
        return User.objects.create_user(**validated_data)

    class Meta:
        """Meta."""

        fields: list = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "photo",
            "level",
            "is_banned",
            "is_trial",
            "profile_completion",
            "works_in",
            "company",
        ]
        read_only_fields: list = [
            "is_banned",
            "is_trial",
            "profile_completion",
            "company",
        ]
        model = User
        extra_kwargs: Dict[str, dict] = {
            "password": {
                "write_only": True
            },
            "photo": {
                "allow_null": True
            },
            "works_in": {
                "allow_null": True
            },
        }
