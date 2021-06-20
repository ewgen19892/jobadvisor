"""Users views."""
from .educations import EducationDetail, EducationList
from .institutes import InstituteList
from .jobs import JobDetail, JobList
from .registration import (
    UserActivation,
    UserInvite,
    UserRegistration,
    UserRestore,
)
from .resumes import ResumeDetail, ResumeList
from .salaries import SalaryList
from .skills import SkillList
from .users import UserDetail, UserList

__all__: list = [
    "EducationDetail",
    "EducationList",
    "InstituteList",
    "JobDetail",
    "JobList",
    "ResumeDetail",
    "ResumeList",
    "UserRegistration",
    "UserRestore",
    "SkillList",
    "UserActivation",
    "UserInvite",
    "UserDetail",
    "UserList",
    "SalaryList",
]
