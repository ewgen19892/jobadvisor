"""Poll filters."""
from django_filters import rest_framework as filters

from jobadvisor.polls.models import Answer, Category, Question


class AnswerFilter(filters.FilterSet):
    """Answer filterset."""

    my = filters.BooleanFilter(method="_is_owner")
    category = filters.ModelMultipleChoiceFilter(
        field_name="question__category",
        queryset=Category.objects.all()
    )
    question = filters.ModelMultipleChoiceFilter(queryset=Question.objects.all())

    class Meta:
        """Meta."""

        model = Answer
        fields: tuple = (
            "company",
        )

    def _is_owner(self, queryset, name, value):
        """
        Filter by owner.

        :param queryset: Categories
        :param name: filter name
        :param value: filter value
        :return: queryset
        """
        del name
        if value:
            return queryset.filter(owner_id=self.request.user.pk)
        return queryset.exclude(owner_id=self.request.user.pk)
