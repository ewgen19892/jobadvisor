"""JobAdvisor URL Configuration."""
from django.contrib import admin
from django.urls import include, path

from django_prometheus.exports import ExportToDjangoView

from .views import index, schema_view

urlpatterns: list = [
    path("admin/", admin.site.urls),
    path("metrics/", ExportToDjangoView, name="metrics"),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="documentation"),
    path("", index, name="index"),
    path("", include("jobadvisor.authentication.urls")),
    path("", include("jobadvisor.users.urls")),
    path("", include("jobadvisor.companies.urls")),
    path("", include("jobadvisor.reviews.urls")),
    path("", include("jobadvisor.polls.urls")),
    path("", include("jobadvisor.landing.urls")),
    path("", include("jobadvisor.notifications.urls")),
]
