"""QA models."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class QA(models.Model):
    """QA model."""

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Question & answer")
        verbose_name_plural: str = _("Questions & answers")

    interview = models.ForeignKey(verbose_name=_("Interview"),
                                  to="reviews.Interview",
                                  on_delete=models.CASCADE,
                                  related_name="qas")
    question = models.TextField(verbose_name=_("Question"))
    answer = models.TextField(verbose_name=_("Answer"))

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self ID
        """
        return f"QA: {self.pk}"
