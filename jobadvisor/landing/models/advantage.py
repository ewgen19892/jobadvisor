"""Landing advantage."""
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from jobadvisor.common.helpers import upload_to
from jobadvisor.users.models.user import User


class Advantage(models.Model):
    """Advantage model."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True
    )
    file = models.ImageField(
        verbose_name=_("File"),
        upload_to=upload_to
    )
    level = models.SmallIntegerField(
        verbose_name=_("User level"),
        choices=User.LEVELS,
        default=User.EMPLOYEE
    )
    weight = models.SmallIntegerField(
        verbose_name=_("Weight"),
        default=1
    )

    class Meta:
        """Meta."""

        ordering: list = ["weight"]
        verbose_name: str = _("Advantage")
        verbose_name_plural: str = _("Advantages")

    def __str__(self) -> str:
        """
        Call as string.

        :return: self name
        """
        return str(self.name)

    @property
    def file_img(self) -> str:
        """
        Get image.

        :return: image tag
        """
        tag = f"<img src='{self.file.url}' width='100' height='50'/>"
        return mark_safe(tag)  # nosec
