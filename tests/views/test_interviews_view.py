from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from tests.factories import (
    CompanyFactory,
    InterviewFactory,
    PositionFactory,
    SubscriptionFactory,
    UserFactory,
)


class InterviewListTestCase(APITestCase):
    fake = Faker()

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory()
        cls.position = PositionFactory()
        cls.interview = InterviewFactory(owner=cls.user)
        for _ in range(cls.fake.random_int(min=10, max=15)):
            InterviewFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.client.force_authenticate(user=self.user)
        self.interview_stub = InterviewFactory.stub(owner=self.user,
                                                    company=self.company,
                                                    position=self.position)
        self.url = reverse("reviews:interview_list")

    def test_interview_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_interview_list_filter_by_company(self):
        response = self.client.get(self.url, data={"company": self.company.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.company.interviews.count())

    def test_interview_create_success(self):
        data = {
            "company": self.interview_stub.company.pk,
            "owner": self.interview_stub.owner.pk,
            "position": self.interview_stub.position.pk,
            "title": self.interview_stub.title,
            "description": self.interview_stub.description,
            "experience": self.interview_stub.experience,
            "complication": self.interview_stub.complication,
            "has_offer": self.interview_stub.has_offer,
            "duration": self.interview_stub.duration,
            "date": self.interview_stub.date,
            "place": self.interview_stub.place,
            "is_anonymous": self.interview_stub.is_anonymous,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_interview_create_bad_request(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class InterviewDetailsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory()
        cls.interview = InterviewFactory(owner=cls.user)

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.interview_stub = InterviewFactory.stub(owner=self.user,
                                                    company=self.company)
        self.url = reverse("reviews:interview_detail",
                           kwargs={"pk": self.interview.pk})

    def test_interview_detail_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_interview_update_success(self):
        data = {
            "company": self.interview_stub.company.pk,
            "owner": self.interview_stub.owner.pk,
            "title": self.interview_stub.title,
            "description": self.interview_stub.description,
            "experience": self.interview_stub.experience,
            "complication": self.interview_stub.complication,
            "has_offer": self.interview_stub.has_offer,
            "duration": self.interview_stub.duration,
            "date": self.interview_stub.date,
            "place": self.interview_stub.place,
            "is_anonymous": self.interview_stub.is_anonymous,
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_interview_update_bad_request(self):
        data = {
            "company": None,
            "owner": self.fake.pyfloat(positive=True),
            "experience": self.fake.sentence(nb_words=8),
            "description": self.user.pk,
            "name": self.fake.text(max_nb_chars=80),
            "website": self.fake.url(),
            "size": self.fake.sentence(nb_words=8),
            "founded": self.fake.date(),
            "is_anonymous": self.fake.paragraph(),
        }
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_interview_is_not_anonymous(self):
        data = {
            "is_anonymous": False,
        }
        response = self.client.patch(self.url, data=data)
        self.assertIsNotNone(response.data["owner"])

    def test_interview_is_anonymous(self):
        data = {
            "is_anonymous": True,
        }
        response = self.client.patch(self.url, data=data)
        self.assertIsNone(response.data["owner"])

    def test_interview_delete_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_interview_delete_permission_denied(self):
        another_user = UserFactory()
        self.client.force_authenticate(user=another_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewFavoriteTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.company = CompanyFactory(owner=cls.user)
        cls.interview = InterviewFactory(owner=cls.user,
                                         company=cls.company,
                                         is_top=False)
        cls.another_user = UserFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.subscription = SubscriptionFactory(company=self.company, plan=2)
        self.url = reverse("reviews:interview_top",
                           kwargs={"pk": self.interview.pk})

    def test_interview_top_add_success(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_top"])

    def test_interview_top_add_no_subscription(self):
        self.company.subscriptions.all().delete()
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_interview_top_add_no_worker(self):
        self.client.force_authenticate(user=self.another_user)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_interview_top_add_exceeded_limit(self):
        for _ in range(self.fake.random_int(min=10, max=15)):
            InterviewFactory(company=self.company, is_top=True)
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_interview_top_remove_success(self):
        self.interview.is_top = True
        self.interview.save()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_top"])


class ReviewHelpfulTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Setup tests data.

        :return:
        """
        cls.user = UserFactory()
        cls.interview = InterviewFactory()

    def setUp(self) -> None:
        """
        Setup tests.

        :return:
        """
        self.fake = Faker()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("reviews:interview_helpful",
                           kwargs={"pk": self.interview.pk})

    def test_interview_helpful_add_success(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_helpful"]["to_me"])

    def test_interview_helpful_remove_success(self):
        self.interview.helpful.add(self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_helpful"]["to_me"])
