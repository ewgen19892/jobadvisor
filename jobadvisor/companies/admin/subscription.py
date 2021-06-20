"""Subscription admin."""
from django.contrib import admin

from jobadvisor.companies.models import Subscription


class SubscriptionInline(admin.StackedInline):
    """Subscription inline admin."""

    model = Subscription
    extra = 0
