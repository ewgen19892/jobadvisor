"""JobAdvisor validators."""
from datetime import date

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError


def past_date(value: date) -> None:
    """
    Сhecks that the date is in the past.

    :param value: date
    :return: None
    """
    if value > date.today():
        raise ValidationError(_("Date cannot be in the future"))
