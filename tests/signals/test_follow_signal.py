import pytest
from tests.factories import FollowFactory

from jobadvisor.notifications.models import Message


@pytest.mark.django_db
def test_follow_signal_create(mocker, company) -> None:
    mocker.spy(Message.objects, "bulk_create")
    FollowFactory(company=company)
    assert Message.objects.bulk_create.call_count == 1
