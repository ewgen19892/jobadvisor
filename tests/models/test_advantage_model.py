"""Test advantage model."""
from tests.factories import AdvantageFactory


def test_advantage_name() -> None:
    advantage = AdvantageFactory.build()
    assert str(advantage) == advantage.name


def test_advantage_file_img_success() -> None:
    advantage = AdvantageFactory.build()
    tag = f"<img src='{advantage.file.url}' width='100' height='50'/>"
    assert advantage.file_img == tag
