"""Users URL Configuration."""
from django.urls import path

from jobadvisor.users.views import (
    EducationDetail,
    EducationList,
    InstituteList,
    JobDetail,
    JobList,
    ResumeDetail,
    ResumeList,
    SalaryList,
    SkillList,
    UserActivation,
    UserDetail,
    UserInvite,
    UserList,
    UserRegistration,
    UserRestore,
)

app_name: str = "users"
urlpatterns: list = [
    path("registration/", UserRegistration.as_view(), name="user_registration"),
    path("activation/<slug:uid>/<slug:token>/", UserActivation.as_view(),
         name="user_activation"),

    path("restore/", UserRestore.as_view(),
         name="user_restore_request"),
    path("restore/<slug:uid>/<slug:token>/", UserRestore.as_view(),
         name="user_restore_finish"),

    path("users/", UserList.as_view(), name="user_list"),
    path("users/<slug:pk>/", UserDetail.as_view(), name="user_detail"),

    path("invite/", UserInvite.as_view(), name="user_invite"),

    path("educations/", EducationList.as_view(), name="education_list"),
    path("educations/<int:pk>/", EducationDetail.as_view(),
         name="education_detail"),

    path("resumes/", ResumeList.as_view(), name="resume_list"),
    path("resumes/<int:pk>/", ResumeDetail.as_view(), name="resume_detail"),

    path("skills/", SkillList.as_view(), name="skill_list"),
    path("institutes/", InstituteList.as_view(), name="institute_list"),

    path("jobs/", JobList.as_view(), name="job_list"),
    path("jobs/<int:pk>/", JobDetail.as_view(), name="job_detail"),

    path("salaries/", SalaryList.as_view(), name="salaries_list"),
]
