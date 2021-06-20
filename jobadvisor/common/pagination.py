"""JobAdvisor paginators."""
from rest_framework import pagination, status
from rest_framework.response import Response


class JobAdvisorPagination(pagination.PageNumberPagination):
    """JobAdvisor paginator."""

    page_size = 6
    page_size_query_param = "page_size"

    def get_paginated_response(self, data: list) -> Response:
        """
        Paginate response.

        :param data: Items list
        :return: Paginated list
        """
        headers = {
            "Link": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "X-Page": self.page.number,
            "X-Per-Page": self.page.paginator.per_page,
            "X-Total": self.page.paginator.count,
            "X-Love": "J+H",
            "Access-Control-Expose-Headers": "Link, X-Page, X-Per-Page, X-Total"
        }
        return Response(data=data, headers=headers, status=status.HTTP_200_OK)
