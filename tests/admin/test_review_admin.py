from django.contrib.admin.sites import AdminSite

from jobadvisor.reviews.admin import ReviewAdmin
from jobadvisor.reviews.models import Review


def test_interview_admin_add_permission(rf):
    request = rf.get("")
    review_admin = ReviewAdmin(model=Review, admin_site=AdminSite())
    assert not review_admin.has_add_permission(request)
