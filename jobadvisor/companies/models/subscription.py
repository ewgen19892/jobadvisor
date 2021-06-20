"""Companies subscription."""
from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from pytz import UTC


class SubscriptionManager(models.Manager):
    """Subscription manager."""

    def get_active(self) -> models.Model:
        """
        Get active subscription.

        :return:
        """
        now = datetime.now(tz=UTC)

        return self.get_queryset().filter(finished_at__gt=now).first()


class Subscription(models.Model):
    """Subscription model."""

    FIRST = 1
    SECOND = 2
    THIRD = 3
    PLANS = (
        (FIRST, _("First")),
        (SECOND, _("Second")),
        (THIRD, _("Third")),
    )

    company = models.ForeignKey(
        verbose_name=_("Company"),
        to="companies.Company",
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )
    plan = models.PositiveIntegerField(
        verbose_name=_("Plan"),
        choices=PLANS
    )
    started_at = models.DateTimeField(
        verbose_name=_("Started at"),
        auto_now_add=True
    )
    finished_at = models.DateTimeField(
        verbose_name=_("Finished at")
    )
    is_trial: bool = models.BooleanField(
        verbose_name=_("Is trial"),
        default=False
    )

    objects = SubscriptionManager()

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Subscription")
        verbose_name_plural: str = _("Subscriptions")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self name
        """
        return f"Subscription: {self.pk}"
