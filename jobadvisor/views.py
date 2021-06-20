"""JobAdvisor views."""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from jobadvisor import __version__


def index(request: HttpRequest) -> HttpResponse:
    """
    Get root.

    :param request:
    :return:
    """
    context = {"version": __version__}
    return render(request, "index.html", context)


schema_view = get_schema_view(
    openapi.Info(
        title="JobAdvisor API",
        default_version=__version__,
        description="Backend",
        contact=openapi.Contact(email="mikalai@mitsin.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
