import pytest

from jobadvisor.companies.tasks import delete_vacancy


@pytest.mark.django_db
def test_delete_vacancy(vacancy) -> None:
    delete_vacancy(pk=vacancy.pk)
    vacancy.refresh_from_db()
    assert vacancy.deleted_at


@pytest.mark.django_db
def test_delete_vacancy_not_found(vacancy, faker) -> None:
    delete_vacancy(pk=faker.pyint())
    vacancy.refresh_from_db()
    assert not vacancy.deleted_at
