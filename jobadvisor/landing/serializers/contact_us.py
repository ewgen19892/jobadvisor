"""Contact us serializers."""
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from jobadvisor.tasks import send_email


class ContactUsSerializer(serializers.Serializer):
    """Contact us serializer."""

    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=16)
    email = serializers.EmailField()
    message = serializers.CharField()

    def create(self, validated_data: dict) -> dict:
        """
        Send email.

        :param validated_data:
        :return: Rating
        """
        send_email.delay(emails=(settings.EMAIL_HOST_USER,),
                         template_name="emails/contact_us.html",
                         context=validated_data,
                         title=_("Contact us"))
        return validated_data
