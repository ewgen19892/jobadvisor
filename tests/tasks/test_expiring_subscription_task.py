import pytest

from jobadvisor.companies.tasks import expiring_subscription
from jobadvisor.notifications.models import Message


@pytest.mark.django_db
def test_expiring_subscription(subscription, mocker) -> None:
    mocker.spy(Message.objects, "bulk_create")
    expiring_subscription(pk=subscription.pk)
    assert Message.objects.bulk_create.call_count == 1


@pytest.mark.django_db
def test_expiring_subscription_not_found(mocker, faker) -> None:
    mocker.spy(Message.objects, "bulk_create")
    expiring_subscription(pk=faker.pyint())
    assert Message.objects.bulk_create.call_count == 0
