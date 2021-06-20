from tests.factories import SubscriptionFactory


def test_subscription_name():
    subscription = SubscriptionFactory.build()
    assert str(subscription) == f"Subscription: {subscription.pk}"
