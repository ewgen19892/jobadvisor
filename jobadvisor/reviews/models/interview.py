"""Interview models."""
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from jobadvisor.reviews.models.report import Report


class Interview(models.Model):
    """Interview model."""

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Interview")
        verbose_name_plural: str = _("Interviews")

    POSITIVE = 2
    NO_OPINION = 1
    NEGATIVE = 0
    EXPERIENCES = (
        (POSITIVE, _("Positive")),
        (NO_OPINION, _("No opinion")),
        (NEGATIVE, _("Negative")),
    )
    company = models.ForeignKey(
        verbose_name=_("Company"),
        to="companies.Company",
        on_delete=models.CASCADE,
        related_name="interviews"
    )
    owner = models.ForeignKey(
        verbose_name=_("Owner"), to="users.User",
        on_delete=models.CASCADE,
        related_name="interviews"
    )
    position = models.ForeignKey(
        verbose_name=_("Position"),
        to="companies.Position",
        on_delete=models.CASCADE,
        related_name="interviews"
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=120
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    experience = models.PositiveSmallIntegerField(
        verbose_name=_("Experience"),
        choices=EXPERIENCES,
        default=NO_OPINION
    )
    complication = models.PositiveSmallIntegerField(
        verbose_name=_("Complication"))
    has_offer = models.BooleanField(
        verbose_name=_("Has offer"),
        null=True
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name=_("duration"),
        help_text=_("In minutes"),
        null=True
    )
    date = models.DateField(
        verbose_name=_("Date"),
        null=True
    )
    place = models.CharField(
        verbose_name=_("Place"),
        max_length=120,
        null=True
    )
    helpful = models.ManyToManyField(
        verbose_name=_("Helpful for this users"),
        to="users.User",
    )
    is_anonymous = models.BooleanField(
        verbose_name=_("Is anonymous"),
        default=True
    )
    is_top = models.BooleanField(
        verbose_name=_("Is TOP"),
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )
    comments = GenericRelation(
        to="reviews.Comment"
    )
    reports = GenericRelation(
        verbose_name=_("Reports"),
        to="reviews.Report"
    )

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self ID
        """
        return f"Interview: {self.pk}"

    def has_report(self) -> bool:
        """
        Check if exists are open reports for this Interview.

        :return: bool
        """
        return self.reports.exclude(status=Report.CLOSED).exists()
