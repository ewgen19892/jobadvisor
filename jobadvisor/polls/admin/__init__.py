"""Polls admin."""
from .answer import AnswerAdmin
from .category import CategoryAdmin
from .question import QuestionAdmin
from .variant import VariantInline

__all__: list = [
    "CategoryAdmin",
    "QuestionAdmin",
    "AnswerAdmin",
    "VariantInline",
]
