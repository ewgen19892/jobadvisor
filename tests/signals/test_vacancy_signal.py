import pytest
from fcm_django.models import FCMDeviceQuerySet

from jobadvisor.notifications.models import Message


@pytest.mark.django_db
def test_vacancy_responded_users(employee, vacancy, mocker) -> None:
    mocker.spy(Message.objects, "bulk_create")
    vacancy.responded_users.add(employee)
    assert Message.objects.bulk_create.call_count == 1


@pytest.mark.django_db
def test_vacancy_responded_users_multiple(employee, vacancy, mocker) -> None:
    mocker.spy(Message.objects, "bulk_create")
    vacancy.responded_users.add(employee)
    vacancy.responded_users.add(employee)
    assert Message.objects.bulk_create.call_count == 1
