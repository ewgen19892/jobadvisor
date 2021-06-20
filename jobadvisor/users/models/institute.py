"""Users institute."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Institute(models.Model):
    """Institute model."""

    name: str = models.CharField(
        verbose_name=_("Institute name"),
        max_length=50,
        unique=True
    )

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Institute")
        verbose_name_plural: str = _("Institutes")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self name
        """
        return str(self.name)
