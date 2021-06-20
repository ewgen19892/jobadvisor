from datetime import datetime

import pytest
import pytz
from tests.factories import (
    AnswerFactory,
    InterviewFactory,
    ReviewFactory,
    UserFactory,
)

from jobadvisor.users.models import User


@pytest.mark.django_db
def test_user_create_user(faker):
    user = User.objects.create_user(email=faker.email(),
                                    password=faker.password())
    assert not user.is_superuser
    assert type(user) is User
    assert not user.is_active
    assert not user.is_banned
    assert not user.is_superuser


def test_user_name():
    user = UserFactory.build()
    assert str(user) == user.get_full_name()


@pytest.mark.django_db
def test_user_create_superuser_success(faker):
    user = User.objects.create_superuser(email=faker.email(),
                                         password=faker.password())
    assert user.is_superuser


@pytest.mark.django_db
def test_user_create_superuser_fail_is_staff(faker):
    with pytest.raises(ValueError):
        User.objects.create_superuser(email=faker.email(),
                                      password=faker.password(),
                                      is_staff=False)


@pytest.mark.django_db
def test_user_create_superuser_fail_is_superuser(faker):
    with pytest.raises(ValueError):
        User.objects.create_superuser(email=faker.email(),
                                      password=faker.password(),
                                      is_superuser=False)


@pytest.mark.django_db
def test_user_profile_completion_trial(employee, polls):
    employee.date_joined = datetime.now(tz=pytz.UTC)
    assert employee.is_trial()


@pytest.mark.django_db
def test_user_profile_completion_zero(faker, employee):
    employee.first_name = None
    employee.last_name = None
    assert employee.profile_completion == 0


@pytest.mark.django_db
def test_user_profile_completion_first_employee(faker, employee, polls):
    assert employee.profile_completion == 1
    assert employee._is_first_level_completion()


@pytest.mark.django_db
def test_user_profile_completion_second_employee(faker, employee, polls):
    ReviewFactory(owner=employee)
    assert employee.profile_completion == 2
    assert employee._is_second_level_completion()


@pytest.mark.django_db
def test_user_profile_completion_second_trainee(faker, trainee, polls):
    InterviewFactory(owner=trainee)
    assert trainee.profile_completion == 2
    assert trainee._is_second_level_completion()


@pytest.mark.django_db
def test_user_profile_completion_second_employer(faker, employee):
    employee.level = None
    assert not employee.profile_completion == 2
    assert not employee._is_second_level_completion()


@pytest.mark.django_db
def test_user_profile_completion_third_employee(faker, employee, company, variant):
    ReviewFactory(owner=employee)
    AnswerFactory(owner=employee,
                  variant=[variant],
                  company=company,
                  question=variant.question)
    assert employee.profile_completion == 3
    assert employee._is_third_level_completion()


@pytest.mark.django_db
def test_user_invite_success(faker):
    user: User = User.objects.invite_user(faker.email())
    assert type(user) is User
    assert not user.is_active
    assert not user.is_banned
    assert not user.is_superuser
    assert user.level == User.EMPLOYER


def test_user_restore_password_success():
    user: User = UserFactory.build()
    user.restore_password()


@pytest.mark.django_db
def test_user_activate_success():
    user: User = UserFactory.build(is_active=False)
    assert not user.is_active
    user.activate()
    assert user.is_active
