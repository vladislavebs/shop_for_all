from abc import abstractmethod
from functools import reduce
from itertools import chain
from typing import Tuple, List

import coreapi
import coreschema
from django.db.models import QuerySet
from django.db.models.sql.constants import ORDER_PATTERN
from django.utils.encoding import force_text
from django.views import View
from rest_framework import filters
from rest_framework.request import Request

from shop_for_all.helpers.methods import is_iterable


class BasicFilter:
    @property
    @abstractmethod
    def schema(self):
        raise NotImplementedError

    @abstractmethod
    def get_query_filters(self, query_params: dict):
        raise NotImplementedError


class Filter(BasicFilter):
    name: str
    filter: str
    core_schema: coreschema
    required: bool = False

    def __init__(
        self,
        name: str,
        query_filter: str,
        schema: coreschema = None,
        required: bool = False,
    ):
        self.name, self.filter, self.required = name, query_filter, required
        self.core_schema = schema or coreschema.Anything(
            title=name, description=f"Filter by {name}."
        )

    @property
    def schema(self):
        return coreapi.Field(
            name=self.name,
            required=self.required,
            location="query",
            schema=self.core_schema,
        )

    def get_query_filters(self, query_params):
        if self.name not in query_params:
            return {}

        return {self.filter: query_params.get(self.name)}


class FiltersGroup(BasicFilter):
    filters: Tuple[Filter]

    def __init__(self, *group_filters: Filter):
        self.filters = group_filters

    @property
    def schema(self):
        return (group_filter.schema for group_filter in self.filters)

    def get_query_filters(self, query_params):
        def _get_query_filters(group_filters: dict, group_filter):
            query_filter = group_filter.get_query_filters(query_params)

            if not query_filter:
                return group_filters

            group_filters.update(query_filter)

            return group_filters

        return reduce(_get_query_filters, self.filters, {})


class OrderingFilter(filters.OrderingFilter):
    def remove_invalid_fields(self, queryset, fields: List[str], view, request):
        # self.get_valid_fields(queryset, view, {'request': request})
        valid_fields = dict(self.get_valid_fields(queryset, view, {"request": request}))

        def get_order_filters(order_filters: list, field: str):
            is_desc = field.startswith("-")

            if is_desc:
                field = field.lstrip("-")

            order_filter = valid_fields.get(field)

            if not (order_filter and ORDER_PATTERN.match(field)):
                return order_filters

            if is_desc:
                order_filter = f"-{order_filter}"

            order_filters.append(order_filter)
            return order_filters

        return reduce(get_order_filters, fields, [])

    def get_schema_fields(self, view):
        default = getattr(view, "ordering_name", getattr(view, "ordering"))

        description = (
            f"{force_text(self.ordering_description)}\nAdd <b>-</b> for descending "
            f"ordering.\n<b><i>Default:</b></i> {default} "
        )

        ordering_fields = list(
            chain.from_iterable(
                (name, f"-{name}")
                for name, _ in self.get_valid_fields(
                    queryset=getattr(view, "queryset", None),
                    view=view,
                    context={"request": view.request},
                )
            )
        )

        # noinspection PyArgumentList
        return [
            coreapi.Field(
                name=self.ordering_param,
                required=False,
                location="query",
                schema=coreschema.Enum(
                    title=force_text(self.ordering_title),
                    description=description,
                    enum=ordering_fields,
                    default=default,
                ),
            )
        ]


class ModelFieldsFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(
        self, request: Request, queryset: QuerySet, view: View
    ) -> QuerySet:
        fields = getattr(view, "fields", None)

        if fields:
            queryset = queryset.filter(**self.create_filters(request, fields))

        return queryset

    def get_schema_fields(self, view):
        fields = getattr(view, "fields", None)

        if not fields:
            return []

        return reduce(self.schema_field, fields, [])

    @staticmethod
    def create_filters(request: Request, fields: iter) -> dict:
        def create_filter(model_filters: dict, field):
            query_filter = field.get_query_filters(request.query_params)

            if not query_filter:
                return model_filters

            model_filters.update(query_filter)
            return model_filters

        return reduce(create_filter, fields, {})

    @staticmethod
    def schema_field(schema_fields, field):
        schema = field.schema

        if is_iterable(schema):
            schema_fields.extend(schema)
        else:
            schema_fields.append(schema)

        return schema_fields
