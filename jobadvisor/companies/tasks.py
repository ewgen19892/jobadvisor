"""Companies tasks."""
from datetime import datetime

from django.utils.translation import gettext_lazy as _

import pytz

from jobadvisor.celery import app
from jobadvisor.companies.models import Subscription, Vacancy
from jobadvisor.notifications.models import Message


@app.task
def expiring_subscription(pk: int) -> None:
    """
    Send notification to all workers.

    :type pk: Subscription pk
    :return: None
    """
    try:
        subscription: Subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        return None
    message = _("Attention! Your subscription is over in 7 day (%(date)s)") % {
        "date": subscription.finished_at.strftime("%B %d, %Y at %H:%M")
    }
    subscription.company.notify_workers(message, Message.INFO)
    return None


@app.task
def delete_vacancy(pk: int) -> None:
    """
    Delete vacancy.

    :param pk: Vacancy pk
    :return: None
    """
    try:
        vacancy = Vacancy.objects.get(pk=pk)
    except Vacancy.DoesNotExist:
        return None
    vacancy.deleted_at = datetime.now(pytz.UTC)
    vacancy.save()
    return None
