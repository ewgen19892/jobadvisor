"""Users skill."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Skill(models.Model):
    """Skill model."""

    name: str = models.CharField(
        verbose_name=_("Name"),
        max_length=50,
        unique=True
    )

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Skill")
        verbose_name_plural: str = _("Skills")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self name
        """
        return str(self.name)
