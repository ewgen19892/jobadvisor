"""Comment admin."""
from django.contrib.contenttypes.admin import GenericTabularInline

from jobadvisor.common.admin import ReadOnlyMixin
from jobadvisor.reviews.models import Comment


class CommentInline(ReadOnlyMixin, GenericTabularInline):
    """Comment inline admin."""

    extra = 0
    model = Comment
    fields = ("owner", "text")
