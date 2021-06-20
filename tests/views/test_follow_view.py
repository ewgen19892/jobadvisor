import pytest
from rest_framework import status
from rest_framework.test import force_authenticate
from tests.factories import CompanyFactory, FollowFactory, SubscriptionFactory

from jobadvisor.companies.views import CompanyFollow


@pytest.mark.django_db
def test_company_follow_get_success(rf, employer):
    company = CompanyFactory(owner=employer)
    SubscriptionFactory(company=company, plan=3)
    follows = FollowFactory.create_batch(10, company=company)
    request = rf.get("", data={"page_size": 100})
    force_authenticate(request, user=employer)
    response = CompanyFollow.as_view()(request, pk=company.pk)
    assert response.status_code == status.HTTP_200_OK
    assert int(response["X-Total"]) == len(follows)


@pytest.mark.django_db
def test_company_follow_add_success(rf, company, employee):
    request = rf.post("")
    force_authenticate(request, user=employee)
    response = CompanyFollow.as_view()(request, pk=company.pk)
    assert response.status_code == status.HTTP_201_CREATED
    assert company in employee.following.all()

@pytest.mark.django_db
def test_company_follow_remove_success(rf, company, employee):
    request = rf.delete("")
    force_authenticate(request, user=employee)
    response = CompanyFollow.as_view()(request, pk=company.pk)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert company not in employee.following.all()
