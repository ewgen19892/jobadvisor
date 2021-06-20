"""Report models."""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class Report(models.Model):
    """Report model."""

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Report")
        verbose_name_plural: str = _("Reports")

    OPEN = 0
    IN_PROGRESS = 1
    CLOSED = 2
    STATUSES = (
        (OPEN, _("Open")),
        (IN_PROGRESS, _("In progress")),
        (CLOSED, _("Closed")),
    )
    owner = models.ForeignKey(verbose_name=_("Owner"),
                              to="users.User",
                              on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_("Text"))
    status = models.PositiveSmallIntegerField(verbose_name=_("Status"),
                                              choices=STATUSES,
                                              default=OPEN)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self ID
        """
        return f"Report: {self.pk}"
