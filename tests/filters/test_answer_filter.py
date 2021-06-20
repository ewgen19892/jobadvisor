import pytest
from rest_framework.request import Request
from rest_framework.test import force_authenticate
from tests.factories import AnswerFactory

from jobadvisor.polls.filters import AnswerFilter
from jobadvisor.polls.models import Answer


@pytest.mark.django_db
def test_answer_filter_is_owner_true(rf, employee):
    AnswerFactory.create_batch(10)
    AnswerFactory.create_batch(5, owner=employee)
    queryset = Answer.objects.all()
    request = rf.get("")
    force_authenticate(request, user=employee)
    filterset = AnswerFilter(request=Request(request))
    filtered_answers = filterset._is_owner(queryset, "my", True)
    assert filtered_answers.count() == employee.answers.count()


@pytest.mark.django_db
def test_answer_filter_is_owner_false(rf, employee):
    AnswerFactory.create_batch(10)
    AnswerFactory.create_batch(5, owner=employee)
    queryset = Answer.objects.all()
    request = rf.get("")
    force_authenticate(request, user=employee)
    filterset = AnswerFilter(request=Request(request))
    filtered_answers = filterset._is_owner(queryset, "my", False)
    assert filtered_answers.count() == queryset.count() - employee.answers.count()
