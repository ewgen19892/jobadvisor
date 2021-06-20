"""Polls views."""
from .answer import AnswerDetail, AnswerList
from .category import CategoryDetail, CategoryList
from .question import QuestionDetail, QuestionList
from .variant import VariantDetail, VariantList

__all__: list = [
    "CategoryDetail",
    "CategoryList",
    "VariantDetail",
    "VariantList",
    "QuestionDetail",
    "QuestionList",
    "AnswerDetail",
    "AnswerList",
]
