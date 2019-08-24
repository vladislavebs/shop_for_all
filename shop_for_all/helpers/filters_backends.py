from functools import reduce

import coreapi
import coreschema
from django.db.models import QuerySet
from django.utils.encoding import force_text
from django.views import View
from rest_framework import filters
from rest_framework.request import Request

# Date created filter
from shop_for_all.helpers.methods import get_index

date_gte_filter = (
    "date_gte",
    "date_created__gte",
    coreschema.String(title="Start date", description="Start date."),
)

date_lte_filter = (
    "date_lte",
    "date_created__lte",
    coreschema.String(title="End date", description="End date."),
)

date_filter = (date_gte_filter, date_lte_filter)


# Amount filter
date_gte_filter = (
    "amount_gte",
    "amount__gte",
    coreschema.String(title="Min amount", description="Min amount."),
)

date_lte_filter = (
    "amount_lte",
    "amount__lte",
    coreschema.Number(title="Max amount", description="Max amount."),
)

amount_filter = (date_gte_filter, date_lte_filter)


class OrderingFilter(filters.OrderingFilter):
    def get_schema_fields(self, view):
        default = getattr(view, "ordering")

        description = (
            f"{force_text(self.ordering_description)}\nAdd <b>-</b> for descending "
            f"ordering.\n<b><i>Default:</b></i> {default} "
        )

        ordering_fields = list(getattr(view, "ordering_fields"))
        ordering_fields = ordering_fields + [f"-{field}" for field in ordering_fields]

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
    @staticmethod
    def get_field_config(field):
        model_field = query_value = field
        schema, required = None, False

        if isinstance(field, tuple):
            query_value, model_field, *additional = field
            schema = get_index(additional, 0)
            required = get_index(additional, 1, False)

        return query_value, model_field, schema, required

    def filter_queryset(
        self, request: Request, queryset: QuerySet, view: View
    ) -> QuerySet:
        fields = getattr(view, "fields", None)

        if fields:
            queryset = queryset.filter(**self.create_filters(request, fields))

        return queryset

    def create_filters(self, request: Request, fields: iter) -> dict:
        def create_filter(model_filters, field):
            query_value, model_field, *_ = self.get_field_config(field)
            filter_value = request.query_params.get(query_value)

            if filter_value is None:
                return model_filters

            return {**model_filters, model_field: filter_value}

        return reduce(create_filter, fields, {})

    def get_schema_fields(self, view):
        fields = getattr(view, "fields", None)

        if not fields:
            return []

        def schema_field(schema_fields, field):
            query_value, model_field, schema, required = self.get_field_config(field)

            if schema is None:
                schema = coreschema.Anything(
                    title=query_value, description=f"Filter by {query_value}."
                )

            # noinspection PyArgumentList
            return [
                *schema_fields,
                coreapi.Field(
                    name=query_value, required=required, location="query", schema=schema
                ),
            ]

        return reduce(schema_field, fields, [])
