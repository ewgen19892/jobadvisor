import pytest
from rest_framework import status
from rest_framework.test import force_authenticate
from tests.factories import MessageFactory

from jobadvisor.notifications.views import MessageList, MessageRead


@pytest.mark.django_db
def test_message_list_success(rf, employee):
    MessageFactory.create_batch(10, owner=employee)
    request = rf.get("", data={"page_size": 100})
    force_authenticate(request, user=employee)
    response = MessageList.as_view()(request)
    assert response.status_code == status.HTTP_200_OK
    assert int(response["X-Total"]) == 10


@pytest.mark.django_db
def test_message_read_success(rf, employee):
    message = MessageFactory(owner=employee, is_read=False)
    request = rf.get("")
    force_authenticate(request, user=employee)
    response = MessageRead.as_view()(request, pk=message.pk)
    message.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_read"]
    assert message.is_read
