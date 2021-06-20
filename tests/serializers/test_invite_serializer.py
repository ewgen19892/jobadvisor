from django.core import mail

import pytest

from jobadvisor.users.models import User
from jobadvisor.users.serializers import InviteSerializer


@pytest.mark.django_db
def test_invite_serializer_create(faker):
    data = {
        "email": faker.email(),
    }
    serializer = InviteSerializer(data=data)
    serializer.is_valid()
    serializer.save()
    assert type(serializer.instance) is User
    assert not serializer.instance.is_active
    assert not serializer.instance.is_banned
    assert not serializer.instance.is_superuser
