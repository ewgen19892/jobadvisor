from rest_framework.test import APITestCase

from jobadvisor.common.admin import ReadOnlyMixin


class ContribEmailTestCase(APITestCase):

    def test_readonly_mixin(self):
        self.assertFalse(ReadOnlyMixin.has_add_permission())
        self.assertFalse(ReadOnlyMixin.has_change_permission())
        self.assertFalse(ReadOnlyMixin.has_delete_permission())
