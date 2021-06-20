import pytest
from rest_framework.exceptions import ValidationError

from jobadvisor.common.validators import past_date


def test_past_date_validator_success(faker):
    assert past_date(faker.past_date()) is None


def test_past_date_validator_fail(faker):
    with pytest.raises(ValidationError):
        past_date(faker.future_date())
