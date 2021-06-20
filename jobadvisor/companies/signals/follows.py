"""Vacancy signals."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from jobadvisor.companies.models import Follow
from jobadvisor.notifications.models import Message


@receiver(post_save, sender=Follow)
def follow_update(instance: Follow, **kwargs) -> None:
    """
    Send notification after create Follow.

    Send notification for all company workers.
    :return:
    """
    if kwargs["created"]:
        message: str = _("%(user_name)s is interested in your company") % {
            "user_name": instance.owner.get_full_name()
        }
        instance.company.notify_workers(message, Message.INFO)
