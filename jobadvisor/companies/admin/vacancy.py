"""Education admin."""
from django.contrib import admin
from django.http import HttpRequest

from jobadvisor.companies.models import Vacancy


class VacancyInline(admin.TabularInline):
    """Education inline admin."""

    model = Vacancy
    fields: tuple = (
        "company",
        "position",
        "description",
        "salary",
        "experience",
        "level",
        "is_hiring",
        "deleted_at",
        "created_at",
    )
    readonly_fields: tuple = (
        "company",
        "position",
        "level",
        "salary",
        "description",
        "experience",
        "created_at",
        "deleted_at",
    )

    can_delete: bool = False

    def has_add_permission(self, request: HttpRequest,
                           obj: Vacancy = None) -> bool:
        """
        Check add permission.

        :param request:
        :param obj:
        :return: False
        """
        return False
