"""Reviews admin."""
from .interview import InterviewAdmin
from .report import ReportAdmin
from .review import ReviewAdmin

__all__: list = [
    "InterviewAdmin",
    "ReportAdmin",
    "ReviewAdmin",
]
