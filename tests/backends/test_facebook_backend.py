"""Test facebook auth backend."""
import facebook
import pytest
from tests.factories import FacebookUserFactory

from jobadvisor.authentication.backends import FacebookBackend
from jobadvisor.authentication.backends.facebook import (
    FacebookException,
    PermissionException,
)


def test_facebook_backend_normalize_user_data_success() -> None:
    raw_data = FacebookUserFactory()
    backend = FacebookBackend()
    normalized_data = backend._normalize_user_data(raw_data)
    assert raw_data["first_name"] == normalized_data["first_name"]
    assert raw_data["last_name"] == normalized_data["last_name"]
    assert raw_data["email"] == normalized_data["email"]
    assert raw_data["picture"]["data"]["url"] == normalized_data["photo_url"]


def test_facebook_backend_normalize_user_data_no_permissions() -> None:
    raw_data = FacebookUserFactory()
    backend = FacebookBackend()
    raw_data.pop("picture")
    with pytest.raises(PermissionException):
        backend._normalize_user_data(raw_data)


def test_facebook_backend_get_user_data_fail(faker) -> None:
    backend = FacebookBackend()
    with pytest.raises(FacebookException):
        backend.get_user_data(faker.sha256())


def test_facebook_backend_get_user_data_success(mocker) -> None:
    mocker.patch.object(facebook.GraphAPI,
                        "get_object",
                        return_value=FacebookUserFactory())
    backend = FacebookBackend()
    user_data = backend.get_user_data("")
    assert "first_name" in user_data
    assert "last_name" in user_data
    assert "email" in user_data
    assert "photo_url" in user_data
