"""Polls models."""
from .answer import Answer
from .category import Category
from .question import Question
from .variant import Variant

__all__: list = [
    "Category",
    "Answer",
    "Question",
    "Variant",
]
