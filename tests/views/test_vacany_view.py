from django.urls import reverse

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from tests.factories import (
    CompanyFactory,
    PositionFactory,
    ResumeFactory,
    SubscriptionFactory,
    UserFactory,
    VacancyFactory,
)

from jobadvisor.companies.models import Subscription
from jobadvisor.companies.views import VacancyDetail, VacancyList
from jobadvisor.users.serializers import UserSerializer


@pytest.mark.django_db
def test_vacancy_list_success(rf, vacancies):
    request = rf.get("")
    response = VacancyList.as_view()(request)
    assert int(response["X-Total"]) == len(vacancies)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_vacancy_create_success(rf):
    user = UserFactory()
    company = CompanyFactory(owner=user)
    position = PositionFactory()
    vacancy_stub = VacancyFactory.stub(company=company, position=position)
    data = {
        "company": vacancy_stub.company.pk,
        "position": vacancy_stub.position.pk,
        "description": vacancy_stub.description,
        "salary": vacancy_stub.salary,
        "experience": vacancy_stub.experience,
        "location": vacancy_stub.location,
        "level": vacancy_stub.level,
    }
    request = rf.post("", data=data)
    force_authenticate(request, user=user)
    response = VacancyList.as_view()(request)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_vacancy_detail_success(rf, vacancy):
    request = rf.get("")
    response = VacancyDetail.as_view()(request, pk=vacancy.pk)
    assert response.status_code == status.HTTP_200_OK
    assert vacancy.description == response.data.get("description")
    assert vacancy.id == response.data.get("id")


@pytest.mark.django_db
def test_vacancy_update_success(rf, vacancy):
    user = vacancy.company.owner
    position = PositionFactory()
    vacancy_stub = VacancyFactory.stub(company=vacancy.company, position=position)
    data = {
        "company": vacancy_stub.company.pk,
        "position": vacancy_stub.position.pk,
        "description": vacancy_stub.description,
        "salary": vacancy_stub.salary,
        "experience": vacancy_stub.experience,
        "location": vacancy_stub.location,
        "level": vacancy_stub.level,
    }
    request = rf.patch("", data=data, content_type='application/json')
    force_authenticate(request, user=user)
    response = VacancyDetail.as_view()(request, pk=vacancy.pk)
    vacancy.refresh_from_db()
    assert response.status_code == status.HTTP_200_OK
    assert vacancy_stub.description == response.data.get("description")


@pytest.mark.django_db
def test_vacancy_delete_success(rf, vacancy):
    request = rf.delete("")
    force_authenticate(request, user=vacancy.company.owner)
    response = VacancyDetail.as_view()(request, pk=vacancy.pk)
    vacancy.refresh_from_db()
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert vacancy.deleted_at is not None


class VacancyFavoriteTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory(owner=cls.user)
        cls.vacancy = VacancyFactory(company=cls.company)
        cls.resume = ResumeFactory(owner=cls.user)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.subscription = SubscriptionFactory(company=self.company,
                                                plan=Subscription.SECOND)
        self.url = reverse("companies:vacancy_response",
                           kwargs={"pk": self.vacancy.pk})

    def test_vacancy_favorites_list_success(self):
        self.vacancy.responded_users.add(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(UserSerializer(self.user).data, response.data)

    def test_vacancy_favorites_add_success(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.vacancy, self.user.responded_vacancies.all())

    def test_vacancy_favorites_remove_success(self):
        self.vacancy.responded_users.add(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.vacancy, self.user.responded_vacancies.all())


class VacancyTopTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory(owner=cls.user)
        cls.vacancy = VacancyFactory(company=cls.company)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.subscription = SubscriptionFactory(company=self.company,
                                                plan=Subscription.THIRD)
        self.url = reverse("companies:vacancy_top",
                           kwargs={"pk": self.vacancy.pk})

    def test_vacancy_top_add_success(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_top"])

    def test_vacancy_top_add_exceeded_limit(self):
        for _ in range(self.fake.random_int(min=2, max=8)):
            VacancyFactory(company=self.company, is_top=True)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_vacancy_top_remove_success(self):
        self.vacancy.is_top = True
        self.vacancy.save()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_top"])
