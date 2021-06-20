from django.contrib.admin.sites import AdminSite

from jobadvisor.companies.admin import VacancyInline
from jobadvisor.companies.models import Vacancy


def test_vacancy_admin_add_permission(rf):
    request = rf.get("")
    vacancy_inline = VacancyInline(parent_model=Vacancy, admin_site=AdminSite())
    assert not vacancy_inline.has_add_permission(request)
