"""Landing serializers."""
from .advantage import AdvantageSerializer
from .contact_us import ContactUsSerializer
from .faq import CategorySerializer, FAQSerializer
from .page import PageSerializer

__all__: list = [
    "AdvantageSerializer",
    "ContactUsSerializer",
    "FAQSerializer",
    "CategorySerializer",
    "PageSerializer",
]
