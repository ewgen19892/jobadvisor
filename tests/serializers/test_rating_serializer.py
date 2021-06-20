from faker import Faker
from rest_framework.test import APITestCase
from tests.factories import RatingFactory

from jobadvisor.companies.serializers.company import RatingSerializer


class RatingSerializerTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """
        SetUp test data.

        :return: None
        """
        cls.serializer = RatingSerializer()

    def setUp(self) -> None:
        """
        SetUp test case.

        :return: None
        """
        self.fake = Faker()

    def test_rating_serializer_create(self) -> None:
        data = RatingFactory()
        serializer = RatingSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(serializer.data, data)

    def test_rating_serializer_update(self) -> None:
        data = RatingFactory()
        new_data = RatingFactory()
        serializer = RatingSerializer(instance=data, data=new_data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(data, new_data)
        self.assertEqual(serializer.data, data)
