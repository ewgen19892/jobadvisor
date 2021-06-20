from tests.factories import SkillFactory


def test_skill_name():
    skill = SkillFactory.build()
    assert str(skill) == str(skill.name)
