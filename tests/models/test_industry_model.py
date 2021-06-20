from tests.factories import IndustryFactory


def test_industry_name() -> None:
    industry = IndustryFactory.build()
    assert str(industry) == industry.name
