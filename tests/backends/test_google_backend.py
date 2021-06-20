"""Test google auth backend."""
import pytest
from tests.factories import GoogleUserFactory

from jobadvisor.authentication.backends import GoogleBackend
from jobadvisor.authentication.backends.google import (
    GoogleException,
    PermissionException,
)


def test_google_backend_normalize_user_data_success() -> None:
    raw_data = GoogleUserFactory()
    backend = GoogleBackend()
    normalized_data = backend._normalize_user_data(raw_data)
    assert raw_data["given_name"] == normalized_data["first_name"]
    assert raw_data["family_name"] == normalized_data["last_name"]
    assert raw_data["email"] == normalized_data["email"]
    assert raw_data["picture"] == normalized_data["photo_url"]

def test_google_backend_normalize_user_data_no_permissions() -> None:
    raw_data = GoogleUserFactory()
    backend = GoogleBackend()
    raw_data.pop("picture")
    with pytest.raises(PermissionException):
        backend._normalize_user_data(raw_data)

def test_google_backend_get_user_data_fail(faker) -> None:
    token = faker.sha256()
    backend = GoogleBackend()
    with pytest.raises(GoogleException):
        backend.get_user_data(token)

def test_google_backend_get_user_data_success(mocker) -> None:
    mocker.patch("google.oauth2.id_token.verify_oauth2_token", return_value=GoogleUserFactory())
    backend = GoogleBackend()
    user_data = backend.get_user_data("")
    assert "first_name" in user_data
    assert "last_name" in user_data
    assert "email" in user_data
    assert "photo_url" in user_data
