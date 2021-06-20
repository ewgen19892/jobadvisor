"""Companies admins."""
from .company import CompanyAdmin
from .industry import IndustryAdmin
from .position import PositionAdmin
from .vacancy import VacancyInline

__all__: list = [
    "CompanyAdmin",
    "IndustryAdmin",
    "PositionAdmin",
    "VacancyInline",
]
