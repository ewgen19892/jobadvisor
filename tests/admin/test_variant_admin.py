from django.contrib.admin.sites import AdminSite

from jobadvisor.polls.admin import VariantInline
from jobadvisor.polls.models import Variant

# def test_variant_admin(rf):
#     request = rf.get("")
#     variant_inline = VariantInline(parent_model=Variant, admin_site=AdminSite())
#     assert not variant_inline.has_add_permission(request)
