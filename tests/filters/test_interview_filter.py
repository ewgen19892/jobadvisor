import pytest
from rest_framework.request import Request
from rest_framework.test import force_authenticate
from tests.factories import InterviewFactory

from jobadvisor.reviews.filters import InterviewFilter
from jobadvisor.reviews.models import Interview


@pytest.mark.django_db
def test_interview_filter_company(rf, interviews, interview, employee):
    queryset = Interview.objects.all()
    filterset = InterviewFilter()
    filtered_interviews = filterset._company(queryset, "company", interview.company.pk)
    assert interview in filtered_interviews
    assert all([r.company.pk == interview.company.pk for r in filtered_interviews])


@pytest.mark.django_db
def test_interview_filter_is_mine_true(rf, interviews, employee):
    interview = InterviewFactory(owner=employee)
    queryset = Interview.objects.all()
    request = rf.get("")
    force_authenticate(request, user=employee)
    filterset = InterviewFilter(request=Request(request))
    filtered_interviews = filterset._is_mine(queryset, "is_mine", True)
    assert interview in filtered_interviews
    assert all([r.owner == employee for r in filtered_interviews])


@pytest.mark.django_db
def test_interview_filter_is_mine_false(rf, interviews, employee):
    interview = InterviewFactory(owner=employee)
    queryset = Interview.objects.all()
    request = rf.get("")
    force_authenticate(request, user=employee)
    filterset = InterviewFilter(request=Request(request))
    filtered_interviews = filterset._is_mine(queryset, "is_mine", False)
    assert interview not in filtered_interviews
    assert all([not r.owner == employee for r in filtered_interviews])
