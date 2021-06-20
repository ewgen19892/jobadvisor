from tests.factories import PositionFactory


def test_position_name():
    position = PositionFactory.build()
    assert str(position) == str(position.name)
