"""Vacancy signals."""
from datetime import datetime, timedelta

from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from jobadvisor.companies.models import Vacancy
from jobadvisor.companies.tasks import delete_vacancy
from jobadvisor.notifications.models import Message
from jobadvisor.users.models import User


@receiver(post_save, sender=Vacancy)
def vacancy_update(instance, **kwargs) -> None:
    """
    Signal create or update.

    :param instance: Vacancy
    :param kwargs: dict
    :return: void
    """
    if kwargs["created"]:
        subscription = instance.company.subscriptions.get_active()
        if subscription.is_trial:
            delete_time = subscription.finished_at
        else:
            delete_time = datetime.now() + timedelta(days=30)
        delete_vacancy.apply_async((instance.pk,), eta=delete_time)


@receiver(m2m_changed, sender=Vacancy.responded_users.through)
def vacancy_responded_users(instance: Vacancy, model, **kwargs) -> None:
    """
    Send notification after add user to the vacancy.

    Send notification for all company workers.
    :param model: User
    :param instance: Vacancy
    :param kwargs:
    :return: None
    """
    if kwargs.get("action") == "post_add":
        user: User = model.objects.filter(id__in=kwargs.get("pk_set")).first()
        if user is None:
            return
        message = _("%(username)s applies for your job %(position)s") % {
            "username": user.get_full_name(),
            "position": instance.position.name
        }
        instance.company.notify_workers(message, Message.SUCCESS)
