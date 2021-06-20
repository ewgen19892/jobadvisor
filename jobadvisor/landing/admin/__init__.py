"""Landing admin."""
from .advantage import AdvantageAdmin
from .faq import CategoryAdmin, FAQAdmin
from .page import PageAdmin

__all__: list = [
    "AdvantageAdmin",
    "CategoryAdmin",
    "FAQAdmin",
    "PageAdmin",
]
