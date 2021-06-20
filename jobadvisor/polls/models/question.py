"""Polls questions."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    """Question model."""

    text = models.TextField(verbose_name=_("Text"))
    category = models.ForeignKey(
        to="polls.Category",
        verbose_name=_("Category"),
        related_name="questions",
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Question")
        verbose_name_plural: str = _("Questions")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self category name and text
        """
        return f"{self.category.name}: {self.text}"
