from django.contrib.admin.sites import AdminSite

from tests.factories import ReviewFactory

from jobadvisor.reviews.admin import ReportAdmin
from jobadvisor.reviews.admin.report import ReportInline
from jobadvisor.reviews.models import Report, Review


def test_report_admin_add_permission(rf):
    request = rf.get("")
    report_admin = ReportAdmin(model=Report, admin_site=AdminSite())
    assert not report_admin.has_add_permission(request)


def test_report_inline_add_permission(rf):
    request = rf.get("")
    report_inline = ReportInline(admin_site=AdminSite(), parent_model=Review)
    assert not report_inline.has_add_permission(request)


def test_report_inline_add_delete(rf):
    request = rf.get("")
    report_inline = ReportInline(parent_model=Review, admin_site=AdminSite())
    assert not report_inline.has_delete_permission(request)


def test_report_inline_owner_email():
    review = ReviewFactory.build()
    report_inline = ReportInline(parent_model=Review, admin_site=AdminSite())
    assert report_inline.owner_email(review) == review.owner.email
