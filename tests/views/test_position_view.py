import pytest
from rest_framework import status
from rest_framework.test import force_authenticate
from tests.factories import PositionFactory, UserFactory

from jobadvisor.companies.views import PositionList


@pytest.mark.django_db
def test_position_list_success(rf, positions):
    request = rf.get("")
    response = PositionList.as_view()(request)
    assert int(response["X-Total"]) == len(positions)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_position_create_success(rf):
    position_stub = PositionFactory.stub()
    data = {
        "name": position_stub.name,
    }
    request = rf.post("", data=data)
    force_authenticate(request, user=UserFactory())
    response = PositionList.as_view()(request)
    assert response.status_code == status.HTTP_201_CREATED
