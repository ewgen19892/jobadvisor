from tests.factories import FollowFactory


def test_follow_name() -> None:
    follow = FollowFactory.build()
    follow_name = f"{follow.owner.get_full_name()} {follow.company.name}"
    assert str(follow) == follow_name
