from django.core.mail import EmailMessage

import pytest

from jobadvisor.tasks import send_email


@pytest.mark.django_db
def test_send_email_success(mocker, faker) -> None:
    mocker.spy(EmailMessage, "send")
    send_email([faker.email()], "emails/signup.html", {})
    assert EmailMessage.send.call_count == 1
