"""Comment serializers."""
from rest_framework import serializers

from jobadvisor.reviews.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""

    class Meta:
        """Meta."""

        model = Comment
        fields: list = [
            "id",
            "owner",
            "text",
        ]
        extra_kwargs: dict = {
            "owner": {
                "read_only": True,
            },
        }
