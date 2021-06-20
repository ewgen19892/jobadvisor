"""Company signals."""
import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from pytz import UTC

from jobadvisor.companies.models import Company, Subscription
from jobadvisor.companies.tasks import expiring_subscription
from jobadvisor.notifications.models import Message


@receiver(post_save, sender=Company)
def company_update(instance, **kwargs) -> None:
    """
    Signal create or update.

    :param instance: Company
    :param kwargs: dict
    :return: void
    """
    if kwargs["created"] and instance.owner:
        finished_at = datetime.datetime.now(tz=UTC) + datetime.timedelta(days=7)
        Subscription.objects.create(company=instance,
                                    plan=Subscription.SECOND,
                                    is_trial=True,
                                    finished_at=finished_at)


@receiver(post_save, sender=Subscription)
def subscription_update(instance: Subscription, **kwargs) -> None:
    """
    Send notification after create Subscription.

    Send notification for all company workers.
    :return:
    """
    if kwargs["created"]:
        message = _("Your subscription succesfully activated! "
                    "You can check your subscription state in “My activities” "
                    "section")
        instance.company.notify_workers(message, Message.SUCCESS)
        notification_date = instance.finished_at - datetime.timedelta(days=7)
        expiring_subscription.apply_async((instance.pk,), eta=notification_date)
