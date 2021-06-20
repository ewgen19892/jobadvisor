"""Users education."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Education(models.Model):
    """Education model."""

    graduated = models.DateField(
        verbose_name=_("Graduated")
    )
    speciality: str = models.CharField(
        verbose_name=_("Speciality"),
        max_length=50
    )
    owner = models.ForeignKey(
        to="users.User",
        verbose_name=_("User"),
        related_name="educations",
        on_delete=models.CASCADE
    )
    institute = models.ForeignKey(
        to="users.Institute",
        verbose_name=_("Institute"),
        related_name="educations",
        on_delete=models.CASCADE
    )

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Education")
        verbose_name_plural: str = _("Educations")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self institute name and speciality
        """
        return f"{self.institute.name} {self.speciality}"
