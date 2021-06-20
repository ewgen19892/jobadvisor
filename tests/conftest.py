import pytest
from faker import Faker
from tests.factories import (
    AdvantageFactory,
    CompanyFactory,
    FAQCategoryFactory,
    FAQFactory,
    IndustryFactory,
    InterviewFactory,
    JobFactory,
    MessageFactory,
    PageFactory,
    PositionFactory,
    QuestionFactory,
    ReviewFactory,
    SubscriptionFactory,
    UserFactory,
    VacancyFactory,
    VariantFactory,
)

from jobadvisor.users.models import User


@pytest.fixture
def industry():
    """
    Create industry

    :return: industry queryset
    """
    return IndustryFactory()


@pytest.fixture
def industries():
    """
    Create industries

    :return: industries queryset
    """
    return IndustryFactory.create_batch(10)


@pytest.fixture
def position():
    """
    Create position

    :return: position
    """
    return PositionFactory()


@pytest.fixture
def positions():
    """
    Create positions

    :return: positions queryset
    """
    return PositionFactory.create_batch(10)


@pytest.fixture
def vacancies():
    """
    Create vacancies

    :return: vacancies queryset
    """
    return VacancyFactory.create_batch(10)


@pytest.fixture
def vacancy():
    """
    Create vacancy

    :return: vacancy queryset
    """
    return VacancyFactory()


@pytest.fixture
def faqs():
    """
    Create jobs

    :return: Jobs queryset
    """
    return FAQFactory.create_batch(10)


@pytest.fixture
def advantages():
    """
    Create advantages

    :return: advantages queryset
    """
    return AdvantageFactory.create_batch(10)


@pytest.fixture
def faq_categories() -> list:
    """
    Create categories

    :return: categories queryset
    """
    return FAQCategoryFactory.create_batch(10)


@pytest.fixture(scope="function")
def faker():
    return Faker()


@pytest.fixture
def employee() -> User:
    """
    Create employee

    :return: Jobs queryset
    """
    user = UserFactory(level=User.EMPLOYEE)
    return user


@pytest.fixture(scope="function")
def employer() -> User:
    """
    Create employee

    :return: Jobs queryset
    """
    user = UserFactory(level=User.EMPLOYER)
    return user


@pytest.fixture
def employee_no_active() -> User:
    """
    Create trainee

    :return: Jobs queryset
    """
    user = UserFactory(level=User.TRAINEE, is_active=False)
    return user


@pytest.fixture
def trainee() -> User:
    """
    Create trainee

    :return: Jobs queryset
    """
    user = UserFactory()
    user.level = User.TRAINEE
    user.save()
    return user


@pytest.fixture
def polls():
    question = QuestionFactory()
    VariantFactory(question=question)


@pytest.fixture
def company():
    return CompanyFactory()


@pytest.fixture
def companies():
    return CompanyFactory.create_batch(10)


@pytest.fixture
def subscription():
    return SubscriptionFactory()


@pytest.fixture
def review():
    return ReviewFactory()


@pytest.fixture
def reviews():
    return ReviewFactory.create_batch(10)


@pytest.fixture
def interview():
    return InterviewFactory()


@pytest.fixture
def interviews():
    return InterviewFactory.create_batch(10)


@pytest.fixture
def page():
    return PageFactory()


@pytest.fixture
def pages():
    return PageFactory.create_batch(10)


@pytest.fixture
def variant():
    return VariantFactory()
