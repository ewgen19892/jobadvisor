import pytest
from tests.factories import CompanyFactory

from jobadvisor.companies.admin.company import CompanyForm


@pytest.mark.django_db
def test_company_form_success(employer):
    data = {
        "owner": employer.pk,
    }
    company_form = CompanyForm(data)
    assert company_form.is_valid()


@pytest.mark.django_db
def test_company_form_employee(employee):
    data = {
        "owner": employee.pk,
    }
    company_form = CompanyForm(data)
    assert not company_form.is_valid()


@pytest.mark.django_db
def test_company_form_user_have_company(employer):
    CompanyFactory(owner=employer)
    data = {
        "owner": employer.pk,
    }
    company_form = CompanyForm(data)
    assert not company_form.is_valid()


@pytest.mark.django_db
def test_company_form_user_have_work(employer):
    company = CompanyFactory()
    employer.workings.add(company)
    data = {
        "owner": employer.pk,
    }
    company_form = CompanyForm(data)
    assert not company_form.is_valid()
