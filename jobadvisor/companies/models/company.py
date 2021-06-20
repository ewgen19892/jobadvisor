"""Companies company."""
from typing import List

from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from jobadvisor.common.helpers import upload_to
from jobadvisor.companies.exceptions import (
    NoActiveSubscription,
    NoRequiredSubscription,
    NotWorker,
)
from jobadvisor.notifications.models import Message
from jobadvisor.polls.models import Answer, Category
from jobadvisor.users.models import User


class Company(models.Model):
    """Company model."""

    owner = models.OneToOneField(
        verbose_name=_("Owner"),
        to="users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="company"
    )
    name: str = models.CharField(
        verbose_name=_("Name"),
        max_length=80,
        unique=True
    )
    industry = models.ForeignKey(
        verbose_name=_("Industry"),
        to="companies.Industry",
        on_delete=models.CASCADE,
        related_name="companies"
    )
    workers = models.ManyToManyField(
        verbose_name=_("Workers"),
        to="users.User",
        related_name="workings"
    )
    logo = models.ImageField(
        verbose_name=_("Logotype"),
        upload_to=upload_to,
        null=True
    )
    website: str = models.URLField(
        verbose_name=_("Website"),
        null=True
    )
    size: int = models.PositiveIntegerField(
        verbose_name=_("Size"),
        null=True
    )
    founded = models.DateField(
        verbose_name=_("Founded date"),
        null=True
    )
    description: str = models.TextField(
        verbose_name=_("Description"),
        null=True
    )
    is_validated: bool = models.BooleanField(
        verbose_name=_("Is validated"),
        default=False
    )
    is_banned: bool = models.BooleanField(
        verbose_name=_("Is banned"),
        default=False
    )
    is_best = models.BooleanField(
        verbose_name=_("This is the best"),
        default=False
    )
    deleted_at: bool = models.DateTimeField(
        verbose_name=_("Deleted at"),
        null=True
    )
    followers = models.ManyToManyField(
        verbose_name=_("followers"),
        to="users.User",
        through="companies.Follow",
        related_name="following"
    )

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]
        verbose_name: str = _("Company")
        verbose_name_plural: str = _("Companies")

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self name
        """
        return str(self.name)

    @property
    def logo_img(self) -> str:
        """
        Get image.

        :return:
        """
        tag = f"<img src='{self.logo.url}' width='100' height='50'/>"
        return mark_safe(tag)  # nosec

    @property
    def owner_phone(self) -> str:
        """
        Get owner phone.

        :return:
        """
        return self.owner.phone if self.owner else None

    @property
    def owner_email(self) -> str:
        """
        Get owner email.

        :return:
        """
        return self.owner.email if self.owner else None

    def get_admin_url(self) -> str:
        """
        Get URL to admin panel.

        :return: Admin URL
        """
        app_label: str = self._meta.app_label
        model_name: str = self._meta.model_name
        return reverse(f"admin:{app_label}_{model_name}_change",
                       args=(self.pk,))

    def has_worker(self, user: User, raise_exception: bool = True) -> bool:
        """
        Check if a user is worker or owner.

        :return:
        """
        if user == self.owner or self.workers.filter(pk=user.pk).exists():
            return True
        if raise_exception:
            raise NotWorker
        return False

    def has_perm(self, permission: int, user: User,
                 raise_exception: bool = True) -> bool:
        """
        Check company permission.

        :param raise_exception:
        :param user:
        :param permission:
        :return:
        """
        if not self.has_worker(user, raise_exception):
            return False
        active_subscription = self.subscriptions.get_active()
        if active_subscription is None:
            if raise_exception:
                raise NoActiveSubscription
            return False
        if active_subscription.plan >= permission:
            return True
        if raise_exception:
            raise NoRequiredSubscription
        return False

    def notify_workers(self, message, level) -> None:
        """
        Notify all company workers.

        :return:
        """
        if not self.owner:
            return
        messages: List[Message] = [Message(owner=worker, level=level, text=message) for
                                   worker in self.workers.iterator()]
        messages.append(Message(owner=self.owner, level=level, text=message))
        Message.objects.bulk_create(messages)

    @property
    def poll_results(self) -> list:
        """
        Get company poll result for each category.

        :return: list
        """
        answers = Answer.objects.filter(company_id=self.id).select_related(
            "question__category")
        results = []

        for category in Category.objects.all():
            # we get all the answers to a specific category
            answers_category = answers.filter(question__category=category)

            # we get the total weight of the answers
            sum_weight = \
                sum([answer.weight for answer in answers_category])

            # calculate percentages
            result = 0
            if answers_category.count():
                result = sum_weight / answers_category.count() * 100

            results.append({"category": category, "result": result})

        return results

    @property
    def rating(self) -> dict:
        """
        Get rating company.

        :return: Dict
        """
        return {"rating": self.reviews.aggregate(Avg("rate"))["rate__avg"],
                "count": self.reviews.count()}
