import pytest
from rest_framework.request import Request
from rest_framework.test import force_authenticate

from jobadvisor.companies.filters import VacancyFilter
from jobadvisor.companies.models import Vacancy


@pytest.mark.django_db
def test_vacancy_filter_is_responded_true(rf, vacancies, vacancy, employee):
    vacancy.responded_users.set([employee])
    queryset = Vacancy.objects.all()
    request = rf.get("")
    force_authenticate(request, user=employee)
    filterset = VacancyFilter(request=Request(request))
    filtered_vacancies = filterset._is_responded(queryset, "is_responded", True)
    assert vacancy in filtered_vacancies
    assert filtered_vacancies.count() == employee.responded_vacancies.count()


@pytest.mark.django_db
def test_vacancy_filter_is_responded_false(rf, vacancies, vacancy, employee):
    vacancy.responded_users.set([employee])
    queryset = Vacancy.objects.all()
    request = rf.get("")
    force_authenticate(request, user=employee)
    filterset = VacancyFilter(request=Request(request))
    filtered_vacancies = filterset._is_responded(queryset, "is_responded", False)
    assert vacancy not in filtered_vacancies
    assert filtered_vacancies.count() == queryset.count() - employee.responded_vacancies.count()
