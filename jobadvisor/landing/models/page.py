"""Landing pages."""
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField


class Page(models.Model):
    """Landing pages."""

    title: str = models.CharField(
        verbose_name=_("Page title"),
        max_length=255
    )
    slug: str = models.SlugField(
        verbose_name=_("Page slug"),
        unique=True,
        help_text=_("Do not change this field")
    )
    text: str = RichTextField(
        verbose_name=_("Page text"),
    )

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self title.
        """
        return self.title

    class Meta:
        """Meta."""

        ordering: tuple = ("pk",)
