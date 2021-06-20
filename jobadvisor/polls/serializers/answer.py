"""Answers serializers."""
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from jobadvisor.polls.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    """Answer serializer."""

    @staticmethod
    def validate_variant(variants: list) -> list:
        """
        Validate variants.

        :param variants:
        :return: Variants
        """
        positive_variant = \
            [variant for variant in variants if variant.is_positive]
        negative_variant = \
            [variant for variant in variants if not variant.is_positive]

        if len(positive_variant) > 1:
            raise serializers.ValidationError(
                _("You can't choose a few positive variants")
            )

        if positive_variant and negative_variant:
            raise serializers.ValidationError(
                _("You can't choose a positive and negative variant")
            )

        return variants

    class Meta:
        """Meta."""

        model = Answer
        fields: list = [
            "id",
            "question",
            "owner",
            "company",
            "variant",
        ]
        extra_kwargs: dict = {
            "owner": {
                "read_only": True,
            },
        }
