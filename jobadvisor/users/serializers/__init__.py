"""User serializers."""
from .education import EducationSerializer
from .institute import InstituteSerializer
from .job import JobSerializer
from .resume import ResumeSerializer
from .salary import SalarySerializer
from .skill import SkillSerializer
from .users import InviteSerializer, UserSerializer

__all__: list = [
    "EducationSerializer",
    "InstituteSerializer",
    "InviteSerializer",
    "JobSerializer",
    "ResumeSerializer",
    "SkillSerializer",
    "UserSerializer",
    "SalarySerializer",
]
