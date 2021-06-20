"""Authentication views."""
from rest_framework_simplejwt.views import TokenViewBase

from jobadvisor.authentication.serializers import (
    ConvertTokenSerializer,
    ObtainTokenPairSerializer,
)


class ConvertToken(TokenViewBase):
    """Convert token view."""

    serializer_class = ConvertTokenSerializer


class TokenObtainPairView(TokenViewBase):
    """Credential authentication view."""

    serializer_class = ObtainTokenPairSerializer
