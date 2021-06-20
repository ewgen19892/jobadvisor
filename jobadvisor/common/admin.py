"""Jobadvisor admin."""


class ReadOnlyMixin:
    """Read only mixin."""

    @staticmethod
    def has_change_permission(request=None, obj=None):
        """
        Check change permission.

        :param request:
        :param obj:
        :return: False
        """
        return False

    @staticmethod
    def has_add_permission(request=None, obj=None):
        """
        Check add permission.

        :param request:
        :param obj:
        :return: False
        """
        return False

    @staticmethod
    def has_delete_permission(request=None, obj=None):
        """
        Check delete permission.

        :param request:
        :param obj:
        :return: False
        """
        return False
