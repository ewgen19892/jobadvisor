"""Test linkedin auth backend."""
import pytest
from tests.factories import (
    LinkedinEmailFactory,
    LinkedinTokenFactory,
    LinkedinUserFactory,
)

from jobadvisor.authentication.backends import LinkedinBackend
from jobadvisor.authentication.backends.linkedin import (
    BadAuthCodeException,
    PermissionException,
)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def test_linkedin_backend_normalize_user_data_success() -> None:
    raw_data = {}
    raw_data.update(LinkedinUserFactory())
    raw_data.update(LinkedinEmailFactory())
    backend = LinkedinBackend()
    normalized_data = backend._normalize_user_data(raw_data)
    assert raw_data["localizedFirstName"] == normalized_data["first_name"]
    assert raw_data["localizedLastName"] == normalized_data["last_name"]


def test_linkedin_backend_normalize_user_data_no_permissions() -> None:
    raw_data = LinkedinUserFactory()
    backend = LinkedinBackend()
    with pytest.raises(PermissionException):
        backend._normalize_user_data(raw_data)


def test_linkedin_backend_auth_fail(faker) -> None:
    token = faker.sha256()
    backend = LinkedinBackend()
    with pytest.raises(BadAuthCodeException):
        backend._auth(token)


def test_linkedin_backend_auth_success(faker, mocker) -> None:
    token = faker.sha256()
    mocker.patch("requests.post", return_value=MockResponse(status_code=200,
                                                            json_data=LinkedinTokenFactory(
                                                                access_token=token)))
    backend = LinkedinBackend()
    backend._auth(token)
    assert backend.token == token


def test_linkedin_backend_get_me_success(mocker) -> None:
    mocker.patch("requests.get", return_value=MockResponse(status_code=200,
                                                           json_data=LinkedinUserFactory()))
    backend = LinkedinBackend()
    user_data = backend._get_me()
    assert "localizedFirstName" in user_data
    assert "localizedLastName" in user_data


def test_linkedin_backend_get_me_fail(mocker) -> None:
    mocker.patch("requests.get",
                 return_value=MockResponse(status_code=401, json_data={}))
    backend = LinkedinBackend()
    with pytest.raises(PermissionException):
        backend._get_me()


def test_linkedin_backend_get_email_success(mocker) -> None:
    mocker.patch("requests.get", return_value=MockResponse(status_code=200,
                                                           json_data=LinkedinEmailFactory()))
    backend = LinkedinBackend()
    user_email = backend._get_email()
    assert not len(user_email) == 0


def test_linkedin_backend_get_email_fail(mocker) -> None:
    mocker.patch("requests.get",
                 return_value=MockResponse(status_code=401, json_data={}))
    backend = LinkedinBackend()
    with pytest.raises(PermissionException):
        backend._get_email()


def test_linkedin_backend_get_user_data(mocker) -> None:
    mocker.patch.object(LinkedinBackend, "_auth", return_value=None)
    mocker.patch.object(LinkedinBackend,
                        "_get_me",
                        return_value=LinkedinUserFactory())
    mocker.patch.object(LinkedinBackend,
                        "_get_email",
                        return_value=LinkedinEmailFactory())
    backend = LinkedinBackend()
    user_data = backend.get_user_data("")
    assert "first_name" in user_data
    assert "last_name" in user_data
    assert "email" in user_data
    assert "photo_url" in user_data
