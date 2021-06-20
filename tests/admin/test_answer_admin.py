from django.contrib.admin.sites import AdminSite

from jobadvisor.polls.admin import AnswerAdmin
from jobadvisor.polls.models import Answer


def test_answer_admin_add_permission(rf):
    request = rf.get("")
    answer_admin = AnswerAdmin(model=Answer, admin_site=AdminSite())
    assert not answer_admin.has_add_permission(request)
