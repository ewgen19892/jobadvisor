from django.contrib.admin.sites import AdminSite

import pytest
from tests.factories import JobFactory

from jobadvisor.users.admin import UserAdmin
from jobadvisor.users.models import User


def test_user_admin_add_permission(rf):
    request = rf.get("")
    user_admin = UserAdmin(model=User, admin_site=AdminSite())
    assert not user_admin.has_add_permission(request)


@pytest.mark.django_db
def test_user_admin_last_salary(employee):
    job = JobFactory(owner=employee)
    assert job.salary == UserAdmin.last_salary(employee)


@pytest.mark.django_db
def test_user_admin_last_level(employee):
    job = JobFactory(owner=employee)
    assert job.get_level_display() == UserAdmin.last_level(employee)
