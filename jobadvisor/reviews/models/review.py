"""Review models."""
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from jobadvisor.reviews.models.report import Report


class Review(models.Model):
    """Review model."""

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Review")
        verbose_name_plural: str = _("Reviews")

    company = models.ForeignKey(
        verbose_name=_("Company"),
        to="companies.Company",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    owner = models.ForeignKey(
        verbose_name=_("Owner"),
        to="users.User",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=120
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    rate = models.FloatField(
        verbose_name=_("Rate"),
    )
    improvements = models.TextField(
        verbose_name=_("Improvements"),
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
    position = models.ForeignKey(
        verbose_name=_("Position"),
        to="companies.Position",
        on_delete=models.CASCADE,
        related_name="reviews",
        null=True,
    )
    started_at = models.DateField(
        verbose_name=_("Started working at"),
        null=True,
    )
    finished_at = models.DateField(
        verbose_name=_("Finished working at"),
        null=True
    )
    is_top = models.BooleanField(
        verbose_name=_("Is TOP"),
        default=False
    )
    is_best = models.BooleanField(
        verbose_name=_("This is the best"),
        default=False
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )
    comments = GenericRelation(
        verbose_name=_("Comments"),
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
        return f"Review: {self.pk}"

    def has_report(self) -> bool:
        """
        Check if exists are open reports for this Review.

        :return: bool
        """
        return self.reports.exclude(status=Report.CLOSED).exists()
