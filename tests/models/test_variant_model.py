from tests.factories import VariantFactory


def test_variant_name():
    variant = VariantFactory.build()
    assert str(variant) == variant.text
