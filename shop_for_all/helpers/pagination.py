from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPaginator(PageNumberPagination):
    invalid_page_message = "{message}"
    page_size_query_param = "per_page"

    def get_paginated_response(self, data):
        return Response(
            {
                "pages": self.page.paginator.num_pages,
                "total": self.page.paginator.count,
                "data": data,
            }
        )
