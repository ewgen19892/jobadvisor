"""Companies serializers."""
from typing import Dict, List, Union

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from jobadvisor.common.validators import past_date
from jobadvisor.companies.models.company import Company
from jobadvisor.companies.models.subscription import Subscription
from jobadvisor.companies.serializers.industry import IndustrySerializer
from jobadvisor.companies.serializers.subscription import (
    SubscriptionSerializer,
)
from jobadvisor.polls.serializers.result import ResultSerializer
from jobadvisor.users.models.user import User
from jobadvisor.users.serializers.users import UserSerializer


class RatingSerializer(serializers.Serializer):
    """Rating serializer."""

    rating = serializers.FloatField()
    count = serializers.IntegerField()

    def create(self, validated_data: dict) -> dict:
        """
        Create rating.

        :param validated_data:
        :return: Rating
        """
        return validated_data

    def update(self, instance: dict, validated_data: dict) -> dict:
        """
        Update rating.

        :param instance:
        :param validated_data:
        :return: Updated rating
        """
        instance["rating"] = validated_data["rating"]
        instance["count"] = validated_data["count"]
        return instance


class CompanySerializer(serializers.ModelSerializer):
    """Company serializer."""

    poll_results = ResultSerializer(
        many=True,
        read_only=True,
    )
    rating = RatingSerializer(
        read_only=True,
    )
    subscription = serializers.SerializerMethodField()

    class Meta:
        """Meta."""

        model = Company
        fields: list = [
            "id",
            "owner",
            "name",
            "industry",
            "workers",
            "logo",
            "website",
            "size",
            "founded",
            "description",
            "is_validated",
            "is_banned",
            "is_best",
            "subscription",
            "poll_results",
            "rating",
        ]
        read_only_fields: tuple = (
            "id",
            "is_validated",
            "is_banned",
            "is_best",
            "subscription",
        )
        extra_kwargs: Dict[str, dict] = {
            "workers": {
                "allow_empty": True,
                "required": False,
            },
            "founded": {
                "validators": [past_date]
            },
        }

    def validate_owner(self, owner: User) -> User:
        """
        Validate company owner.

        :param owner:
        :return: Owner
        """
        if self.instance and self.instance.owner and \
                not self.instance.owner == owner:
            raise serializers.ValidationError(
                _("You can't change the owner"))
        if owner and not owner.level == User.EMPLOYER:
            raise serializers.ValidationError(
                _("Only the employer can be the owner"))
        if owner and owner.workings.exists():
            raise serializers.ValidationError(
                _("Owner should not have works"))
        return owner

    def validate_workers(self, workers: List[User]) -> List[User]:
        """
        Validate workers list.

        :param workers: Workers list
        :return: Workers
        """
        if not self.instance:
            return []
        company_workers = self.instance.workers.all()
        for worker in workers:
            if worker not in company_workers:
                if not worker.level == User.EMPLOYER:
                    raise serializers.ValidationError(
                        {worker.pk: _(
                            "User must be an employer to become an worker")})
                if hasattr(worker, "company"):
                    raise serializers.ValidationError(
                        {worker.pk: _("User should not have companies")})
                if worker.workings.exists():
                    raise serializers.ValidationError(
                        {worker.pk: _("User should not have works")})
        return workers

    def get_subscription(self, instance: Company) -> Union[dict, None]:
        """
        Get company subscriptions.

        If user from the context is an worker of the company, return active
        subscription of the company, otherwise - null.
        :param instance:
        :return:
        """
        request = self.context.get("request")
        if not request:
            return None
        if instance.has_worker(request.user, raise_exception=False):
            subscription: Subscription = instance.subscriptions.get_active()
            if subscription:
                return SubscriptionSerializer(instance=subscription).data
        return None

    def to_representation(self, instance: Company) -> dict:
        """
        Transform object.

        :param instance: Company
        :return: OrderedDict
        """
        self.fields["industry"] = IndustrySerializer()
        self.fields["workers"] = UserSerializer(many=True)
        return super().to_representation(instance)
