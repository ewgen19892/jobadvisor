"""Comment models."""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    """Comment model."""

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Comment")
        verbose_name_plural: str = _("Comments")

    owner = models.ForeignKey(verbose_name=_("Owner"),
                              to="users.User",
                              on_delete=models.CASCADE,
                              related_name="comments")
    text = models.TextField(verbose_name=_("Text"))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self ID
        """
        return f"Comment: {self.pk}"
