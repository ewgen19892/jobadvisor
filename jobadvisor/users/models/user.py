"""Users models."""
from datetime import datetime
from typing import Any, Optional

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.db.models import Count
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from jobadvisor.common.helpers import upload_to
from jobadvisor.polls.models import Question
from jobadvisor.tasks import send_email


class UserManager(BaseUserManager):
    """User manager."""

    use_in_migrations = True

    def _create_user(self, email: Optional[str], password: Optional[str],
                     username: Optional[str] = None,
                     **extra_fields: Any) -> AbstractUser:
        """
        Create and save a user with the given username, email, and password.

        :param email:
        :param password:
        :param username:
        :param extra_fields:
        :return:
        """
        del username
        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,
                    username: str = None,
                    email: str = None,
                    password: str = None,
                    **extra_fields: Any) -> AbstractUser:
        """
        Create user.

        :param username:
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self._create_user(username=username,
                                 email=email,
                                 password=password,
                                 **extra_fields)
        token = default_token_generator.make_token(user)
        context = {
            "level": user.level,
            "token": token,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        }
        send_email.delay([email], "emails/signup.html", context)
        return user

    def invite_user(self, email: str) -> AbstractUser:
        """
        Invite user to JobAdvisor.

        :param email:
        :return:
        """
        user = self._create_user(username=None,
                                 email=email,
                                 password=None,
                                 is_staff=False,
                                 is_superuser=False,
                                 level=User.EMPLOYER)
        token = default_token_generator.make_token(user)
        context = {
            "user_name": user.get_full_name(),
            "token": token,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        }
        send_email.delay([email], "emails/invite.html", context)
        return user

    def create_superuser(self,
                         email: str,
                         password: str,
                         username: str = None,
                         **extra_fields: Any) -> AbstractUser:
        """
        Create superuser.

        :param email:
        :param password:
        :param username:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username=username, email=email,
                                 password=password, **extra_fields)


class User(AbstractUser):
    """User model."""

    TRAINEE: int = 0
    EMPLOYEE: int = 1
    EMPLOYER: int = 2
    LEVELS: tuple = (
        (TRAINEE, _("Trainee")),
        (EMPLOYEE, _("Employee")),
        (EMPLOYER, _("Employer")),
    )
    username = None
    email: str = models.EmailField(
        verbose_name=_("Email address"),
        unique=True
    )
    first_name: str = models.CharField(
        verbose_name=_("First name"),
        max_length=30,
        null=True
    )
    last_name: str = models.CharField(
        verbose_name=_("Last name"),
        max_length=150,
        null=True
    )
    phone: str = models.CharField(
        verbose_name=_("Phone number"),
        max_length=15,
        null=True
    )
    photo = models.ImageField(
        upload_to=upload_to,
        null=True,
        max_length=255
    )
    level: int = models.PositiveIntegerField(
        verbose_name=_("Level"),
        choices=LEVELS,
        default=EMPLOYEE
    )
    is_banned: bool = models.BooleanField(
        verbose_name=_("Is banned"),
        default=False
    )
    is_active: bool = models.BooleanField(
        verbose_name=_("Active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects: UserManager = UserManager()

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list = []

    class Meta:
        """Meta."""

        ordering: list = ["-pk"]

    def __str__(self) -> str:
        """
        Call as string.

        :return: Self full name
        """
        return self.get_full_name()

    def _is_first_level_completion(self) -> bool:
        """
        Check user on first level completion.

        :return: first level completion.
        """
        return bool(self.first_name and self.last_name)

    def _is_second_level_completion(self) -> bool:
        """
        Check user on second level completion.

        :return: second level completion.
        """
        if self.level == self.EMPLOYEE:
            return self.reviews.exists()
        if self.level == self.TRAINEE:
            return self.interviews.exists()
        return False

    def _is_third_level_completion(self) -> bool:
        """
        Check user on third level completion.

        :return: third level completion.
        """
        answers = self.answers.order_by("company_id").values("company_id").annotate(
            count=Count("company_id"))
        question_count = Question.objects.count()
        return any([i["count"] >= question_count for i in answers])

    def is_trial(self) -> bool:
        """
        Check user on trial level completion.

        :return: first trial completion.
        """
        now = datetime.utcnow().timestamp()
        trial = now - 604800 if self.level == self.EMPLOYER else now - 86400
        return trial <= self.date_joined.timestamp()

    @property
    def profile_completion(self) -> int:
        """
        Get profile completion.

        :return: profile completion level.
        """
        completion: int = 0
        if self.level == self.EMPLOYER or self.is_trial():
            completion = 3
            return completion
        if self._is_first_level_completion():
            completion = 1
        if self._is_second_level_completion():
            completion = 2
        if self._is_third_level_completion():
            completion = 3
        return completion

    def restore_password(self) -> None:
        """
        Restore password for this user.

        Send email to the user with restore token.
        :return: None
        """
        token = default_token_generator.make_token(self)
        context = {
            "user_name": self.get_full_name(),
            "token": token,
            "uid": urlsafe_base64_encode(force_bytes(self.pk)),
        }
        send_email.delay([self.email], "emails/reset_password.html", context)

    def activate(self) -> None:
        """
        Activate this user.

        :return:
        """
        self.is_active = True
        self.save()

    @property
    def works_in(self):
        """
        Get current company for this user.

        :return: Company
        """
        return self.workings.last().pk if self.workings.exists() else None
