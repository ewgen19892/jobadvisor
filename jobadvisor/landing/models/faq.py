"""Landing FAQ."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from jobadvisor.users.models import User


class Category(models.Model):
    """Category model."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=50,
        unique=True,
    )

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Category")
        verbose_name_plural: str = _("Categories")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self name
        """
        return f"{self.name}"


class FAQ(models.Model):
    """FAQ model."""

    category = models.ForeignKey(
        to="Category",
        verbose_name=_("Category"),
        related_name="faq",
        on_delete=models.SET_NULL,
        null=True,
    )
    level = models.IntegerField(
        verbose_name=_("Level"),
        help_text=_("Select level"),
        choices=User.LEVELS,
    )
    question = models.TextField(verbose_name=_("Question"))
    answer = models.TextField(verbose_name=_("Answer"))

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("FAQ")
        verbose_name_plural: str = _("FAQ")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self category and question
        """
        return f"{self.category}: {self.question}"
