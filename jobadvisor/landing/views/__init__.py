"""Landing views."""
from .advantage import AdvantageList
from .contact_us import ContactUs
from .faq import CategoryList, FAQDetail, FAQList
from .page import PageDetail, PageList

__all__: list = [
    "AdvantageList",
    "ContactUs",
    "FAQList",
    "FAQDetail",
    "CategoryList",
    "PageList",
    "PageDetail",
]
