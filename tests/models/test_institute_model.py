from tests.factories import InstituteFactory


def test_institute_name():
    institute = InstituteFactory.build()
    assert str(institute) == str(institute.name)
