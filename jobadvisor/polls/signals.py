"""Poll signals."""
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from jobadvisor.polls.models import Variant


# pylint: disable=unused-argument
@receiver(post_save, sender=Variant)
def calculate_weight(sender: Variant,
                     instance: Variant,
                     **kwargs: dict) -> None:
    """
    Calculate weight for variant.

    :param sender:
    :param instance:
    :param kwargs:
    :return: None
    """
    del sender
    qs_variant = Variant.objects.filter(pk=instance.pk)

    if instance.is_positive:
        qs_variant.update(weight=1)
        return

    negative_variants = Variant.objects.filter(
        question_id=instance.question_id,
        is_positive=False,
    )

    if negative_variants.count() == 1:
        negative_variants.update(weight=0)
        return

    if negative_variants.count() > 1:
        count_negative_variants = negative_variants.count()
        weight = 1 / count_negative_variants
        negative_variants.update(weight=weight)


# pylint: disable=unused-argument
@receiver(post_delete, sender=Variant)
def recalculate_weight(sender: Variant,
                       instance: Variant,
                       **kwargs: dict) -> None:
    """
    Recalculate weight for variant.

    :param sender:
    :param instance:
    :param kwargs:
    :return: None
    """
    del sender

    if instance.is_positive:
        return

    negative_variants = Variant.objects.filter(
        question_id=instance.question_id,
        is_positive=False,
    )

    if negative_variants.count() == 1:
        negative_variants.update(weight=0)
        return

    if negative_variants.count() > 1:
        count_negative_variants = negative_variants.count()
        weight = 1 / count_negative_variants
        negative_variants.update(weight=weight)
