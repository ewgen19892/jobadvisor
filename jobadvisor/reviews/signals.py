"""Reviews signals."""
from typing import List

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from jobadvisor.notifications.models import Message
from jobadvisor.reviews.models import Comment, Interview, Report, Review
from jobadvisor.users.models import User


@receiver(post_save, sender=Review)
def review_update(instance: Review, **kwargs) -> None:
    """
    Send notification after create Review.

    Send notification for all company workers.
    :return:
    """
    if kwargs["created"]:
        user_name: str = _("Anonymous Author")
        if not instance.is_anonymous:
            user_name = instance.owner.get_full_name()
        message = _("%(user_name)s published new review of your company") % {
            "user_name": user_name,
        }
        instance.company.notify_workers(message, Message.INFO)


@receiver(post_save, sender=Interview)
def interview_update(instance: Interview, **kwargs) -> None:
    """
    Send notification after create Interview.

    Send notification for all company workers.
    :return:
    """
    if kwargs["created"]:
        username: str = _("Anonymous Author")
        if not instance.is_anonymous:
            username = instance.owner.get_full_name()
        message = _("%(username)s published new interview of your company") % {
            "username": username,
        }
        instance.company.notify_workers(message, Message.INFO)


@receiver(post_save, sender=Comment)
def comment_save(instance: Comment, **kwargs) -> None:
    """
    Send notification after create Comment.

    Send notification for review/interview owner.
    :param instance: Comment
    :param kwargs:
    :return: None
    """
    if kwargs["created"]:
        message: str = _("%(company_name)s answered on your %(type)s") % {
            "company_name": instance.content_object.company.name,
            "type": str(instance.content_type).lower(),
        }
        Message.objects.create(owner=instance.content_object.owner,
                               level=Message.INFO,
                               text=message)


@receiver(post_save, sender=Report)
def report_save(instance: Report, **kwargs) -> None:
    """
    Send notification after create Report.

    Send notification for review/interview owner.
    :param instance: Comment
    :param kwargs:
    :return: None
    """
    if kwargs["created"]:
        message: str = _("Created report on the %(type)s") % {
            "type": str(instance.content_type).lower(),
        }
        admins = User.objects.filter(is_superuser=True).all()
        messages: List[Message] = [
            Message(owner=admin, level=Message.WARNING, text=message) for
            admin in admins]
        Message.objects.bulk_create(messages)
