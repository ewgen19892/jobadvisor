import pytest
from rest_framework.request import Request
from rest_framework.test import force_authenticate
from tests.factories import FollowFactory

from jobadvisor.companies.filters import CompanyFilter
from jobadvisor.companies.models import Company


@pytest.mark.django_db
def test_company_filter_is_follow_true(rf, companies, company, employee):
    FollowFactory(company=company, owner=employee)
    queryset = Company.objects.all()
    request = rf.get("")
    force_authenticate(request, user=employee)
    filterset = CompanyFilter(request=Request(request))
    filtered_companies = filterset._is_following(queryset, "is_follow", True)
    assert company in filtered_companies
    assert filtered_companies.count() == 1


@pytest.mark.django_db
def test_company_filter_is_follow_false(rf, companies, company, employee):
    FollowFactory(company=company, owner=employee)
    queryset = Company.objects.all()
    request = rf.get("")
    force_authenticate(request, user=employee)
    filterset = CompanyFilter(request=Request(request))
    filtered_companies = filterset._is_following(queryset, "is_follow", False)
    assert company not in filtered_companies
    assert filtered_companies.count() == queryset.count() - 1
