"""Vacancy serializers."""
from rest_framework import serializers

from jobadvisor.companies.models import Company, Subscription, Vacancy
from jobadvisor.companies.serializers.company import CompanySerializer
from jobadvisor.companies.serializers.position import PositionSerializer
from jobadvisor.users.models import User


class VacancySerializer(serializers.ModelSerializer):
    """Vacancy serializer."""

    is_responded = serializers.SerializerMethodField()

    class Meta:
        """Meta."""

        model = Vacancy
        fields: list = [
            "id",
            "company",
            "position",
            "description",
            "salary",
            "experience",
            "location",
            "level",
            "is_top",
            "is_responded",
            "created_at",
            "deleted_at",
            "responses_count",
        ]
        read_only_fields: tuple = (
            "responses_count",
            "receptive",
            "is_top",
            "is_responded",
        )

    def validate_company(self, company: Company) -> Company:
        """
        Check permission on the company.

        :param company:
        :return: Company
        """
        if company:
            company.has_perm(Subscription.SECOND, self.context["request"].user)
        return company

    def get_is_responded(self, obj: Vacancy) -> bool:
        """
        Check if this user already responded for this vacancy.

        :return: bool
        """
        request = self.context.get("request")
        if not request or not request.user or request.user.is_anonymous:
            return False
        return obj.responded_users.filter(pk=request.user.pk).exists()

    def add_response(self, user: User) -> Vacancy:
        """
        Add response.

        :param user: User
        :return: Vacancy
        """
        self.instance.responded_users.add(user)
        return self.instance

    def remove_response(self, user: User):
        """
        Remove response.

        :param user: User
        :return: Vacancy
        """
        self.instance.responded_users.remove(user)
        return self.instance

    def to_representation(self, instance: Vacancy) -> dict:
        """
        Transform object.

        :param instance: Vacancy
        :return: OrderedDict
        """
        self.fields["position"] = PositionSerializer()
        self.fields["company"] = CompanySerializer()
        return super().to_representation(instance)
