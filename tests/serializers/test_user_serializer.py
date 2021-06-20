import pytest

from jobadvisor.users.models import User
from jobadvisor.users.serializers import UserSerializer


@pytest.mark.django_db
def test_user_serializer_create(faker):
    data = {
        "email": faker.email(),
        "password": faker.password(),
    }
    serializer = UserSerializer(data=data)
    serializer.is_valid()
    serializer.save()
    assert type(serializer.instance) is User
    assert not serializer.instance.is_active
    assert not serializer.instance.is_banned
    assert not serializer.instance.is_superuser
