"""User filters."""
from django_filters import rest_framework as filters

from jobadvisor.companies.models import Company, Position


class SalaryFilter(filters.FilterSet):
    """Salary filterset."""

    company = filters.ModelMultipleChoiceFilter(
        field_name="jobs__company",
        queryset=Company.objects.all()
    )

    class Meta:
        """Meta."""

        model = Position
        fields: tuple = tuple()
