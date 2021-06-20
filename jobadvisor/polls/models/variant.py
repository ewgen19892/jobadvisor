"""Answer variants."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Variant(models.Model):
    """Variant model."""

    question = models.ForeignKey(
        to="polls.Question",
        verbose_name=_("Question"),
        related_name="variants",
        on_delete=models.CASCADE,
    )
    is_positive = models.BooleanField(
        verbose_name=_("Is positive"),
        default=False,
    )
    weight = models.FloatField(
        verbose_name=_("Weight"),
        default=0.0,
        validators=[
            MinValueValidator(limit_value=0.0),
            MaxValueValidator(limit_value=1.0),
        ],
    )
    text = models.TextField(verbose_name=_("Text"))

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Variant")
        verbose_name_plural: str = _("Variants")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self text
        """
        return self.text
