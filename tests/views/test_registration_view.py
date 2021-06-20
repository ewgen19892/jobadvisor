from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import pytest
from rest_framework import status
from rest_framework.test import force_authenticate

from jobadvisor.users.models import User
from jobadvisor.users.views import UserActivation, UserInvite, UserRegistration


@pytest.mark.django_db
def test_users_registration_success(faker, rf):
    data = {
        "email": faker.email(),
        "password": faker.md5(raw_output=False),
    }
    request = rf.post("", data=data)
    response = UserRegistration.as_view()(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email=data["email"]).exists()


@pytest.mark.django_db
def test_users_registration_bad_request(faker, rf):
    data = {
        "email": faker.first_name(),
        "password": faker.md5(raw_output=False),
    }
    request = rf.post("", data=data)
    response = UserRegistration.as_view()(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_users_activate_success(rf, employee_no_active):
    token = default_token_generator.make_token(employee_no_active)
    uid = urlsafe_base64_encode(force_bytes(employee_no_active.pk))
    request = rf.get("")
    response = UserActivation.as_view()(request, uid=uid, token=token)
    employee_no_active.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert employee_no_active.is_active


@pytest.mark.django_db
def test_users_activate_not_found(faker, rf, employee_no_active):
    token = default_token_generator.make_token(employee_no_active)
    uid = urlsafe_base64_encode(
        force_bytes(faker.pyint(min_value=employee_no_active.pk)))
    request = rf.get("")
    response = UserActivation.as_view()(request, uid=uid, token=token)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert not employee_no_active.is_active


@pytest.mark.django_db
def test_users_activate_invalid_token(faker, rf, employee_no_active):
    token = faker.md5(raw_output=False)
    uid = urlsafe_base64_encode(force_bytes(employee_no_active.pk))
    request = rf.get("")
    response = UserActivation.as_view()(request, uid=uid, token=token)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not employee_no_active.is_active


@pytest.mark.django_db
def test_users_invite_success(faker, rf, employer):
    data = {
        "email": faker.email(),
    }
    request = rf.post("", data=data)
    force_authenticate(request, user=employer)
    response = UserInvite.as_view()(request)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email=data["email"]).exists()
