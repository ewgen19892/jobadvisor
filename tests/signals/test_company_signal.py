import pytest
from tests.factories import CompanyFactory

from jobadvisor.companies.models import Subscription


@pytest.mark.django_db
def test_company_signal_create_subscription() -> None:
    company = CompanyFactory()
    subscription: Subscription = company.subscriptions.get_active()
    assert subscription
    assert subscription.plan == Subscription.SECOND
