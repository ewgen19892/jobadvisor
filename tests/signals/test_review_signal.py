import pytest
from fcm_django.models import FCMDeviceQuerySet
from tests.factories import ReviewFactory

from jobadvisor.notifications.models import Message


@pytest.mark.django_db
def test_review_signal_create(mocker, company) -> None:
    mocker.spy(Message.objects, "bulk_create")
    ReviewFactory(company=company)
    assert Message.objects.bulk_create.call_count == 1
