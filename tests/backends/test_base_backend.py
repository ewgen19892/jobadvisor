"""Test base auth backend."""
import os

import pytest
from tests.factories import NormalizedUserFactory

from jobadvisor.authentication.backends.base import BaseBackend
from jobadvisor.users.models import User


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.headers = {"content-type": "jpg"}
        self.content = b"image"


def test_base_backend_get_user_data_success() -> None:
    backend = BaseBackend()
    with pytest.raises(NotImplementedError):
        backend.get_user_data("")


@pytest.mark.django_db
def test_base_backend_update_photo(mocker, faker, employee):
    mocker.patch("requests.get",
                 return_value=MockResponse(status_code=200, json_data={}))
    BaseBackend.update_photo(faker.image_url(), employee)
    employee.refresh_from_db()
    assert os.path.isfile(employee.photo.path)


@pytest.mark.django_db
def test_base_backend_get_user_success(mocker) -> None:
    mocker.patch.object(BaseBackend,
                        "get_user_data",
                        return_value=NormalizedUserFactory())
    mocker.patch.object(BaseBackend,
                        "update_photo",
                        return_value=None)
    backend = BaseBackend()
    user, is_created = backend.get_user("")
    assert type(user) is User


@pytest.mark.django_db
def test_base_backend_get_user_without_photo_success(mocker) -> None:
    mocker.patch.object(BaseBackend,
                        "get_user_data",
                        return_value=NormalizedUserFactory(photo_url=None))
    backend = BaseBackend()
    user, is_created = backend.get_user("")
    assert type(user) is User
