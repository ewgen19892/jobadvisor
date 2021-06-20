"""Users job."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Job(models.Model):
    """Favorite  model."""

    TRAINEE: int = 0
    EMPLOYEE: int = 1
    LEVELS: tuple = (
        (TRAINEE, _("Trainee")),
        (EMPLOYEE, _("Employee")),
    )

    owner = models.ForeignKey(
        verbose_name=_("Owner"), to="users.User",
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    company = models.ForeignKey(
        verbose_name=_("Company"),
        to="companies.Company",
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    position = models.ForeignKey(
        verbose_name=_("Position"),
        to="companies.Position",
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    level: int = models.PositiveIntegerField(
        verbose_name=_("Level"),
        choices=LEVELS,
        default=EMPLOYEE
    )
    salary: int = models.PositiveIntegerField(
        verbose_name=_("Salary")
    )
    started_at = models.DateField(
        verbose_name=_("Started working at")
    )
    finished_at = models.DateField(
        verbose_name=_("Finished working at"),
        null=True
    )

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Job")
        verbose_name_plural: str = _("Jobs")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self company name and position
        """
        return f"{self.company.name} {self.position}"
