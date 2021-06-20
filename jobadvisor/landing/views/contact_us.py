"""Contact us views."""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from jobadvisor.landing.serializers import ContactUsSerializer


class ContactUs(APIView):
    """Contact us view."""

    serializer_class = ContactUsSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        Send contact us email.

        :param request: Request
        :return: Contact form
        """
        serializer = self.serializer_class(data=request.data,
                                           context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
