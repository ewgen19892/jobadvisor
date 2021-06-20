from django.contrib.admin.sites import AdminSite

from jobadvisor.reviews.admin import InterviewAdmin
from jobadvisor.reviews.models import Interview


def test_interview_admin_add_permission(rf):
    request = rf.get("")
    interview_admin = InterviewAdmin(model=Interview, admin_site=AdminSite())
    assert not interview_admin.has_add_permission(request)
