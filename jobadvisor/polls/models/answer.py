"""Answers on questions."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Answer(models.Model):
    """Answer model."""

    question = models.ForeignKey(
        to="polls.Question",
        verbose_name=_("Question"),
        related_name="answers",
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        to="users.User",
        verbose_name=_("Owner"),
        related_name="answers",
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        to="companies.Company",
        verbose_name=_("Company"),
        related_name="answers",
        on_delete=models.CASCADE,
    )
    variant = models.ManyToManyField(
        to="polls.variant",
        verbose_name=_("Variant"),
        related_name="answers",
    )

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Answer")
        verbose_name_plural: str = _("Answers")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self full user name and question
        """
        return f"{self.owner.get_full_name()}. {self.weight}"

    @property
    def weight(self) -> float:
        """
        Get answer weight.

        :return: weight
        """
        positive_variants = self.variant.filter(is_positive=True)
        negative_variants = self.variant.filter(is_positive=False)
        weight = 1.0  # Maximum answer weight

        if positive_variants.exists():
            return weight

        if negative_variants.count() == 1 \
                and negative_variants.first().weight == 0:
            return 0.0

        for variant in negative_variants:
            weight -= variant.weight

        return weight
