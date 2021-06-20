from tests.factories import CategoryFactory


def test_category_name() -> None:
    category = CategoryFactory.build()
    assert str(category) == category.name
