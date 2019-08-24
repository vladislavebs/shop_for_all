from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.inspectors.base import PaginatorInspector as _PaginatorInspector


class PaginatorInspector(_PaginatorInspector):
    def get_paginated_response(self, paginator, response_schema):
        paged_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict(
                (
                    ("pages", openapi.Schema(type=openapi.TYPE_INTEGER)),
                    ("total", openapi.Schema(type=openapi.TYPE_INTEGER)),
                    ("data", response_schema),
                )
            ),
            required=["pages", "total", "data"],
        )

        return paged_schema
