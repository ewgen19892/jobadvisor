from django.contrib.contenttypes.models import ContentType

import factory
from factory.django import DjangoModelFactory
from pytz import UTC

from jobadvisor.authentication.serializers import ConvertTokenSerializer
from jobadvisor.companies.models import (
    Company,
    Follow,
    Industry,
    Position,
    Subscription,
    Vacancy,
)
from jobadvisor.landing.models import (
    FAQ,
    Advantage,
    Category as FAQCategory,
    Page,
)
from jobadvisor.notifications.models import Message
from jobadvisor.polls.models import Answer, Category, Question, Variant
from jobadvisor.reviews.models import QA, Comment, Interview, Report, Review
from jobadvisor.users.models import (
    Education,
    Institute,
    Job,
    Resume,
    Skill,
    User,
)


class UserFactory(DjangoModelFactory):
    """User factory."""

    class Meta:
        """Meta."""

        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    level = factory.Iterator((User.TRAINEE, User.EMPLOYER, User.EMPLOYEE))
    date_joined = factory.Faker("past_datetime", start_date="-30d")
    is_superuser = False
    is_active = True


class AdminFactory(DjangoModelFactory):
    """Admin factory."""

    class Meta:
        """Meta."""

        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_superuser = True


class FacebookUserFactory(factory.Factory):
    """Facebook user factory."""

    class Meta:
        model = dict

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    picture = factory.DictFactory(
        data=factory.DictFactory(url=factory.Faker("image_url")))


class GoogleUserFactory(factory.Factory):
    """Google user factory."""

    class Meta:
        model = dict

    iss = factory.Faker("domain_name")
    azp = factory.Faker("domain_name")
    sub = factory.Faker("domain_name")
    email = factory.Faker("email")
    email_verified = factory.Faker("boolean")
    at_hash = factory.Faker("md5")
    name = factory.Faker("name")
    picture = factory.Faker("image_url")
    given_name = factory.Faker("first_name")
    family_name = factory.Faker("last_name")
    locale = factory.Faker("language_code")
    iat = factory.Faker("unix_time")
    exp = factory.Faker("unix_time")
    jti = factory.Faker("sha1")


class LinkedinUserFactory(factory.Factory):
    """Linkedin user factory."""

    class Meta:
        model = dict

    localizedFirstName = factory.Faker("first_name")
    localizedLastName = factory.Faker("last_name")


class LinkedinEmailFactory(factory.Factory):
    """Linkedin email factory."""

    class Meta:
        model = dict

    elements = [{"handle~": {"emailAddress": factory.Faker("email")}}]


class LinkedinTokenFactory(factory.Factory):
    """Linkedin token factory."""

    class Meta:
        model = dict

    access_token = factory.Faker("sha256")


class NormalizedUserFactory(factory.Factory):
    """Normalized user factory."""

    class Meta:
        model = dict

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    photo_url = factory.Faker("image_url")


class TokenFactory(factory.Factory):
    """Token factory."""

    class Meta:
        model = dict

    token = factory.Faker("sha256")
    backend = factory.Iterator(
        (ConvertTokenSerializer.FACEBOOK, ConvertTokenSerializer.GOOGLE))


class FacebookTokenFactory(TokenFactory):
    """Facebook token factory."""

    backend = ConvertTokenSerializer.FACEBOOK


class GoogleTokenFactory(TokenFactory):
    """Google token factory."""

    backend = ConvertTokenSerializer.GOOGLE


class LinkedinTokenFactory(TokenFactory):
    """Linkedin token factory."""

    backend = ConvertTokenSerializer.LINKEDIN


class IndustryFactory(DjangoModelFactory):
    """Industry factory."""

    class Meta:
        """Meta."""

        model = Industry

    name = factory.Faker("text", max_nb_chars=50)


class PositionFactory(DjangoModelFactory):
    """Position factory."""

    class Meta:
        """Meta."""

        model = Position

    name = factory.Faker("text", max_nb_chars=50)


class CompanyFactory(DjangoModelFactory):
    """Company factory."""

    class Meta:
        """Meta."""

        model = Company

    owner = factory.SubFactory(UserFactory)
    name = factory.Faker("text", max_nb_chars=80)
    industry = factory.SubFactory(IndustryFactory)
    logo = factory.django.ImageField()
    website = factory.Faker("url")
    size = factory.Faker("random_int", min=1)
    founded = factory.Faker("date_between", start_date="-30y", end_date="today")
    description = factory.Faker("paragraph")
    is_validated = factory.Faker("boolean")
    is_best = factory.Faker("boolean")
    is_banned = False
    deleted_at = None


class VacancyFactory(DjangoModelFactory):
    """Position factory."""

    class Meta:
        """Meta."""

        model = Vacancy

    company = factory.SubFactory(CompanyFactory)
    position = factory.SubFactory(PositionFactory)
    description = factory.Faker("paragraph")
    salary = factory.Faker("random_int", min=1)
    experience = factory.Faker("pyfloat", positive=True)
    location = factory.Faker("sentence", nb_words=8)
    level = factory.Iterator((Vacancy.TRAINEE, Vacancy.EMPLOYEE))
    is_top = factory.Faker("boolean")
    is_hiring = factory.Faker("boolean")
    created_at = factory.Faker("date_time", tzinfo=UTC)
    deleted_at = None


class SubscriptionFactory(DjangoModelFactory):
    """Subscription factory."""

    class Meta:
        """Meta."""

        model = Subscription

    company = factory.SubFactory(CompanyFactory)
    plan = factory.Iterator(
        (Subscription.FIRST, Subscription.SECOND, Subscription.THIRD))
    started_at = factory.Faker("past_datetime", tzinfo=UTC)
    finished_at = factory.Faker("future_datetime", tzinfo=UTC)


class FollowFactory(DjangoModelFactory):
    """Follow factory."""

    class Meta:
        """Meta."""

        model = Follow

    company = factory.SubFactory(CompanyFactory)
    owner = factory.SubFactory(UserFactory)
    description = factory.Faker("paragraph")


class RatingFactory(factory.Factory):
    """Rating factory."""

    class Meta:
        model = dict

    rating = factory.Faker("pyfloat")
    count = factory.Faker("random_int", min=1)


class FAQCategoryFactory(DjangoModelFactory):
    """Category factory."""

    class Meta:
        """Meta."""

        model = FAQCategory

    name = factory.Faker("text", max_nb_chars=50)


class FAQFactory(DjangoModelFactory):
    """FAQ factory."""

    class Meta:
        """Meta."""

        model = FAQ

    category = factory.SubFactory(FAQCategoryFactory)
    question = factory.Faker("paragraph")
    answer = factory.Faker("text", max_nb_chars=50)
    level = factory.Iterator((User.EMPLOYEE, User.TRAINEE, User.EMPLOYER))


class AdvantageFactory(DjangoModelFactory):
    """Advantage factory."""

    class Meta:
        """Meta."""

        model = Advantage

    name = factory.Faker("text", max_nb_chars=255)
    file = factory.django.ImageField()
    weight = factory.Faker("random_int", min=0, max=31415)
    level = factory.Iterator((User.EMPLOYEE, User.TRAINEE, User.EMPLOYER))


class CategoryFactory(DjangoModelFactory):
    """Category factory."""

    class Meta:
        """Meta."""

        model = Category

    name = factory.Faker("text", max_nb_chars=50)


class QuestionFactory(DjangoModelFactory):
    """Question factory."""

    class Meta:
        """Meta."""

        model = Question

    text = factory.Faker("text")
    category = factory.SubFactory(CategoryFactory)


class VariantFactory(DjangoModelFactory):
    """Variant factory."""

    class Meta:
        """Meta."""

        model = Variant

    question = factory.SubFactory(QuestionFactory)
    is_positive = factory.Faker("boolean")
    weight = factory.Faker("pyfloat", positive=True)
    text = factory.Faker("text")


class AnswerFactory(DjangoModelFactory):
    """Answer factory."""

    class Meta:
        """Meta."""

        model = Answer

    question = factory.SubFactory(QuestionFactory)
    owner = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)

    @factory.post_generation
    def variant(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for variant in extracted:
                self.variant.add(variant)


class ReviewFactory(DjangoModelFactory):
    """Review factory."""

    class Meta:
        """Meta."""

        model = Review

    company = factory.SubFactory(CompanyFactory)
    owner = factory.SubFactory(UserFactory)
    title = factory.Faker("text", max_nb_chars=120)
    description = factory.Faker("paragraph")
    rate = factory.Faker("pyfloat", positive=True)
    improvements = factory.Faker("paragraph")
    is_anonymous = factory.Faker("boolean")
    position = factory.SubFactory(PositionFactory)
    started_at = factory.Faker("date_between", start_date="-30y", end_date="-10y")
    finished_at = factory.Faker("date_between", start_date="-9y", end_date="today")
    is_top = factory.Faker("boolean")
    is_best = False


class InterviewFactory(DjangoModelFactory):
    """Interview factory."""

    class Meta:
        """Meta."""

        model = Interview

    company = factory.SubFactory(CompanyFactory)
    owner = factory.SubFactory(UserFactory)
    position = factory.SubFactory(PositionFactory)
    title = factory.Faker("text", max_nb_chars=120)
    description = factory.Faker("paragraph")
    experience = factory.Iterator(
        (Interview.POSITIVE, Interview.NO_OPINION, Interview.NEGATIVE))
    complication = factory.Faker("random_int", max=999, min=1)
    has_offer = factory.Faker("boolean")
    duration = factory.Faker("random_int", max=999, min=1)
    date = factory.Faker("date")
    place = factory.Faker("text", max_nb_chars=120)
    is_anonymous = factory.Faker("boolean")
    is_top = factory.Faker("boolean")


class QAFactory(DjangoModelFactory):
    """QA factory."""

    class Meta:
        """Meta."""

        model = QA

    interview = factory.SubFactory(InterviewFactory)
    question = factory.Faker("paragraph")
    answer = factory.Faker("paragraph")


class CommentedItemFactory(factory.django.DjangoModelFactory):
    """CommentedItemFactory factory."""

    class Meta:
        """Meta."""

        exclude = ["content_object"]
        abstract = True

    owner = factory.SubFactory(UserFactory)
    text = factory.Faker("paragraph")
    object_id = factory.SelfAttribute("content_object.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))


class CommentedReviewFactory(CommentedItemFactory):
    """Commented review factory."""

    content_object = factory.SubFactory(ReviewFactory)

    class Meta:
        """Meta."""

        model = Comment


class CommentedInterviewFactory(CommentedItemFactory):
    """Commented interview factory."""

    content_object = factory.SubFactory(InterviewFactory)

    class Meta:
        """Meta."""

        model = Comment


class ReportedItemFactory(factory.django.DjangoModelFactory):
    """Reported item factory."""

    class Meta:
        """Meta."""

        model = Report
        exclude = ["content_object"]
        abstract = True

    owner = factory.SubFactory(UserFactory)
    text = factory.Faker("paragraph")
    status = factory.Iterator((Report.OPEN, Report.IN_PROGRESS, Report.CLOSED))
    object_id = factory.SelfAttribute("content_object.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))


class ReportedReviewFactory(ReportedItemFactory):
    """Reported review factory."""

    content_object = factory.SubFactory(ReviewFactory)


class ReportedInterviewFactory(ReportedItemFactory):
    """Reported interview factory."""

    content_object = factory.SubFactory(InterviewFactory)


class SkillFactory(DjangoModelFactory):
    """Skill factory."""

    class Meta:
        """Meta."""

        model = Skill

    name = factory.Faker("sentence", nb_words=3)


class InstituteFactory(DjangoModelFactory):
    """Institute factory."""

    class Meta:
        """Meta."""

        model = Institute

    name = factory.Faker("sentence", nb_words=3)


class ResumeFactory(DjangoModelFactory):
    """Resume factory."""

    class Meta:
        """Meta."""

        model = Resume

    file = factory.django.FileField(filename="fixtures/test_file.docx")
    experience = factory.Faker("pyfloat", positive=True)
    certificates = factory.Faker("sentence", nb_words=8)
    description = factory.Faker("paragraph")
    salary = factory.Faker("random_int", min=1)
    owner = factory.SubFactory(UserFactory)


class EducationFactory(DjangoModelFactory):
    """Education factory."""

    class Meta:
        """Meta."""

        model = Education

    graduated = factory.Faker("date")
    speciality = factory.Faker("sentence", nb_words=3)
    institute = factory.SubFactory(InstituteFactory)
    owner = factory.SubFactory(UserFactory)


class JobFactory(DjangoModelFactory):
    """Job factory."""

    class Meta:
        """Meta."""

        model = Job

    owner = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)
    position = factory.SubFactory(PositionFactory)
    level = factory.Iterator((Job.EMPLOYEE, Job.TRAINEE))
    salary = factory.Faker("random_int", min=1)
    started_at = factory.Faker("date_between", start_date="-30y", end_date="-10y")
    finished_at = factory.Faker("date_between", start_date="-9y", end_date="today")


class PageFactory(DjangoModelFactory):
    """Page factory."""

    class Meta:
        """Meta."""

        model = Page

    title = factory.Faker("sentence", nb_words=8)
    slug = factory.Faker("slug")
    text = factory.Faker("paragraph")


class MessageFactory(DjangoModelFactory):
    """Message factory."""

    class Meta:
        """Meta."""

        model = Message

    owner = factory.SubFactory(UserFactory)
    text = factory.Faker("sentence", nb_words=8)
    is_read = factory.Faker("boolean")
    level = factory.Iterator((Message.WARNING, Message.INFO, Message.MESSAGE,
                              Message.SUCCESS, Message.ALARM))
