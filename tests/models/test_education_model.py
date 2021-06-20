from tests.factories import EducationFactory


def test_education_name():
    education = EducationFactory.build()
    education_name: str = f"{education.institute.name} {education.speciality}"
    assert str(education) == education_name
