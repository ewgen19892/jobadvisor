"""Companies vacancy."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Vacancy(models.Model):
    """Vacancy model."""

    TRAINEE = 0
    EMPLOYEE = 1
    CANDIDATE_LEVELS = (
        (TRAINEE, _("Trainee")),
        (EMPLOYEE, _("Employee")),
    )

    company = models.ForeignKey(
        verbose_name=_("Company"),
        to="companies.Company",
        on_delete=models.CASCADE,
        related_name="vacancies"
    )
    position = models.ForeignKey(
        verbose_name=_("Position"),
        to="companies.Position",
        on_delete=models.CASCADE,
        related_name="vacancies"
    )
    description = models.TextField(
        verbose_name=_("Description")
    )
    salary = models.PositiveIntegerField(
        verbose_name=_("Salary")
    )
    experience = models.FloatField(
        verbose_name=_("Experience in years")
    )
    location = models.CharField(
        verbose_name=_("Location"),
        max_length=255
    )
    level = models.SmallIntegerField(
        verbose_name=_("Candidate level"),
        choices=CANDIDATE_LEVELS,
        default=EMPLOYEE
    )
    is_top = models.BooleanField(
        verbose_name=_("Participates in the top"),
        default=False
    )
    responded_users = models.ManyToManyField(
        to="users.User",
        related_name="responded_vacancies",
    )
    is_hiring = models.BooleanField(
        verbose_name=_("Is hiring"),
        default=False
    )
    deleted_at = models.DateTimeField(
        verbose_name=_("Deleted at"),
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )

    class Meta:
        """Meta."""

        ordering: list = ["-is_top", "-pk"]
        verbose_name: str = _("Vacancy")
        verbose_name_plural: str = _("Vacancies")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self company name and position name
        """
        return f"{self.company.name} {self.position.name}"

    @property
    def responses_count(self) -> int:
        """
        Get responses count.

        :return: responses count
        """
        return self.responded_users.count()
