"""Companies URL Configuration."""
from django.urls import path

from jobadvisor.companies.views import (
    CompanyDetail,
    CompanyFollow,
    CompanyList,
    IndustryList,
    PositionList,
    VacancyDetail,
    VacancyList,
    VacancyResponse,
    VacancyTop,
)

app_name: str = "companies"
urlpatterns: list = [
    path("positions/", PositionList.as_view(), name="position_list"),
    path("industries/", IndustryList.as_view(), name="industry_list"),

    path("companies/", CompanyList.as_view(), name="company_list"),
    path("companies/<int:pk>/", CompanyDetail.as_view(), name="company_detail"),
    path("companies/<int:pk>/follow/", CompanyFollow.as_view(),
         name="company_follow"),

    path("vacancies/", VacancyList.as_view(), name="vacancy_list"),
    path("vacancies/<int:pk>/", VacancyDetail.as_view(), name="vacancy_detail"),
    path("vacancies/<int:pk>/response/", VacancyResponse.as_view(),
         name="vacancy_response"),
    path("vacancies/<int:pk>/top/", VacancyTop.as_view(),
         name="vacancy_top"),
]
