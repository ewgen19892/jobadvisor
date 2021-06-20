from django.contrib.admin.sites import AdminSite

from jobadvisor.companies.admin import CompanyAdmin
from jobadvisor.companies.models import Company


def test_company_admin_add_permission(rf):
    request = rf.get("")
    company_admin = CompanyAdmin(model=Company, admin_site=AdminSite())
    assert not company_admin.has_add_permission(request)
