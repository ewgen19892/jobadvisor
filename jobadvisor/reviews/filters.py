"""Reviews filters."""
from django_filters import rest_framework as filters

from jobadvisor.reviews.models import Interview, Review


class ReviewFilter(filters.FilterSet):
    """Review filterset."""

    company = filters.NumberFilter(method="_company")
    is_mine = filters.BooleanFilter(method="_is_mine")

    class Meta:
        """Meta."""

        model = Review
        fields: tuple = (
            "is_best",
        )

    @staticmethod
    def _company(queryset, name, value):
        """
        Filter by company.

        :param queryset: Reviews queryset
        :param name: filter name
        :param value: filter value
        :return: queryset
        """
        del name
        if value:
            queryset = queryset.filter(company_id=value).order_by("-is_top", "-pk")
        return queryset

    def _is_mine(self, queryset, name, value):
        """
        Filter by owner.

        :param queryset: Reviews queryset
        :param name: filter name
        :param value: filter value
        :return: queryset
        """
        del name
        if value:
            return queryset.filter(owner_id=self.request.user.pk)
        return queryset.exclude(owner_id=self.request.user.pk)


class InterviewFilter(filters.FilterSet):
    """Interview filterset."""

    company = filters.NumberFilter(method="_company")
    is_mine = filters.BooleanFilter(method="_is_mine")

    class Meta:
        """Meta."""

        model = Interview
        fields: tuple = (
            "has_offer",
            "is_anonymous",
            "complication",
            "experience",
            "position",
        )

    @staticmethod
    def _company(queryset, name, value):
        """
        Filter and order by company.

        :param queryset: Reviews queryset
        :param name: filter name
        :param value: filter value
        :return: queryset
        """
        del name
        if value:
            queryset = queryset.filter(company_id=value).order_by("-is_top", "-pk")
        return queryset

    def _is_mine(self, queryset, name, value):
        """
        Filter by owner.

        :param queryset: Reviews queryset
        :param name: filter name
        :param value: filter value
        :return: queryset
        """
        del name
        if value:
            return queryset.filter(owner_id=self.request.user.pk)
        return queryset.exclude(owner_id=self.request.user.pk)
