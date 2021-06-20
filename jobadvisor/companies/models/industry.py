"""Companies industry."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Industry(models.Model):
    """Industry model."""

    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True)

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Industry")
        verbose_name_plural: str = _("Industry")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self name
        """
        return str(self.name)
