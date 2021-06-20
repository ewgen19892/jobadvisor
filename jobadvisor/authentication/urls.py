"""Authentication URL Configuration."""
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from jobadvisor.authentication.views import ConvertToken, TokenObtainPairView

app_name: str = "authentication"

urlpatterns: list = [
    path("auth/convert/", ConvertToken.as_view(), name="convert_token"),
    path("auth/token/", TokenObtainPairView.as_view(), name="obtain_token"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
]
