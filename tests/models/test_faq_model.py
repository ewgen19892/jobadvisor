"""Test FAQ."""

from tests.factories import FAQCategoryFactory, FAQFactory


def test_category_name() -> None:
    category = FAQCategoryFactory.build()
    assert str(category) == category.name


def test_faq_name() -> None:
    faq = FAQFactory.build()
    assert str(faq) == f"{faq.category}: {faq.question}"
