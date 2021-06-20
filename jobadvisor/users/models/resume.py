"""Users resume."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from jobadvisor.common.helpers import upload_to


class Resume(models.Model):
    """Resume model."""

    file = models.FileField(
        verbose_name=_("File"),
        upload_to=upload_to
    )
    position = models.ForeignKey(
        verbose_name=_("Position"),
        to="companies.Position",
        on_delete=models.SET_NULL,
        null=True,
        related_name="resumes"
    )
    experience: float = models.FloatField(
        verbose_name=_("Experience in years")
    )
    certificates: str = models.TextField(
        verbose_name=_("Certificates"),
        null=True
    )
    description: str = models.TextField(
        verbose_name="Description",
        null=True
    )
    salary: int = models.PositiveIntegerField(
        verbose_name="Salary"
    )
    owner = models.OneToOneField(
        verbose_name=_("User"),
        to="users.User",
        related_name="resumes",
        on_delete=models.CASCADE
    )
    skills = models.ManyToManyField(
        verbose_name=_("Skills"),
        to="users.Skill",
        related_name="resumes"
    )

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Resume")
        verbose_name_plural: str = _("Resumes")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self full user name and position
        """
        return f"{self.owner.get_full_name()} {self.position}"
