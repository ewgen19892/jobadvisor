"""Users favorite companies."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Follow(models.Model):
    """Favorite  model."""

    owner = models.ForeignKey(
        verbose_name=_("Owner"),
        to="users.User",
        on_delete=models.CASCADE,
        related_name="follows"
    )
    company = models.ForeignKey(
        verbose_name=_("Company"),
        to="companies.Company",
        on_delete=models.CASCADE,
        related_name="follows"
    )
    description: str = models.TextField(
        verbose_name=_("Description"),
        null=True
    )

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Favorite")
        verbose_name_plural: str = _("Favorites")
        unique_together: tuple = ("owner", "company")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self full name and company name
        """
        return f"{self.owner.get_full_name()} {self.company.name}"
