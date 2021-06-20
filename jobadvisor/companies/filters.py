"""Companies filters."""
from django_filters import rest_framework as filters

from jobadvisor.companies.models import Company, Vacancy


class VacancyFilter(filters.FilterSet):
    """Vacancy filterset."""

    salary_gte = filters.NumberFilter(field_name="salary", lookup_expr="gte")
    salary_lte = filters.NumberFilter(field_name="salary", lookup_expr="lte")
    experience_gte = filters.NumberFilter(field_name="experience", lookup_expr="gte")
    experience_lte = filters.NumberFilter(field_name="experience", lookup_expr="lte")
    is_deleted = filters.BooleanFilter(field_name="deleted_at",
                                       lookup_expr="isnull",
                                       exclude=True)
    is_responded = filters.BooleanFilter(method="_is_responded")

    class Meta:
        """Meta."""

        model = Vacancy
        fields: tuple = (
            "company",
            "location",
            "position",
            "is_hiring",
            "level",
        )

    def _is_responded(self, queryset, name, value):
        """
        Filter vacancies by responded users.

        :param queryset: Vacancies queryset
        :param name: filter name
        :param value: filter value
        :return: Filtered queryset
        """
        del name
        if value:
            return queryset.filter(responded_users__id=self.request.user.pk)
        return queryset.exclude(responded_users__id=self.request.user.pk)


class CompanyFilter(filters.FilterSet):
    """Company filterset."""

    is_following = filters.BooleanFilter(method="_is_following")

    class Meta:
        """Meta."""

        model = Company
        fields: tuple = (
            "owner",
            "is_best",
        )

    def _is_following(self, queryset, name, value):
        """
        Filter vacancies by followers.

        :param queryset: Companies queryset
        :param name: filter name
        :param value: filter value
        :return: Filtered queryset
        """
        del name
        if value:
            return queryset.filter(followers__id=self.request.user.pk)
        return queryset.exclude(followers__id=self.request.user.pk)
