from tests.factories import VacancyFactory


def test_vacancy_name():
    vacancy = VacancyFactory.build()
    vacancy_name: str = f"{vacancy.company.name} {vacancy.position.name}"
    assert str(vacancy) == vacancy_name
