"""Test advantage model."""
from tests.factories import MessageFactory


def test_message_name() -> None:
    message = MessageFactory.build()
    assert str(message) == message.text
