"""Users admin."""
from .education import EducationInline
from .institute import InstituteAdmin
from .job import JobInline
from .resume import ResumeInline
from .skill import SkillAdmin
from .user import UserAdmin

__all__: list = [
    "EducationInline",
    "InstituteAdmin",
    "JobInline",
    "ResumeInline",
    "SkillAdmin",
    "UserAdmin",
]
