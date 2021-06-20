import pytest
from rest_framework import status

from jobadvisor.landing.views import AdvantageList


@pytest.mark.django_db
def test_advantage_list_success(rf, advantages):
    request = rf.get("", data={"page_size": 100})
    response = AdvantageList.as_view()(request)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(advantages)
