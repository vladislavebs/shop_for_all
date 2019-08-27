import typing
from functools import wraps

from rest_framework import serializers
from rest_framework.decorators import action as action_drf

from shop_for_all.helpers.drf_yasg import update_auto_schema


class MultiSerializers:
    serializer_classes: typing.Dict[str, serializers.Serializer]
    action: str = None

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)


def action(*args, **kwargs):
    serializer_class = kwargs.get("serializer_class")
    partial = kwargs.pop("partial", False)
    query_serializer_class = kwargs.pop("query_serializer_class", None)
    action_decorator = action_drf(*args, **kwargs)

    def decorator(view_func):
        def wrapper(obj, request, *_args, **_kwargs):
            serializer_context = obj.get_serializer_context()

            if serializer_class:
                serializer = serializer_class(
                    data=request.data, context=serializer_context, partial=partial
                )
                serializer.is_valid(raise_exception=True)
                request.serializer = serializer

            if query_serializer_class:
                query_serializer = query_serializer_class(
                    data=request.query_params,
                    context=serializer_context,
                    partial=partial,
                )
                query_serializer.is_valid(raise_exception=True)
                request.query_serializer = query_serializer

            return view_func(obj, request, *_args, **_kwargs)

        auto_schema = {}

        if serializer_class:
            auto_schema["request_body"] = serializer_class

        if query_serializer_class:
            auto_schema["query_serializer"] = query_serializer_class

        if auto_schema:
            update_auto_schema(view_func, auto_schema)

        return wraps(action_decorator(view_func))(wrapper)

    return decorator


def create_serializer(data=None, initialize=True):
    serializer = type("", (serializers.Serializer,), data or {})

    if initialize:
        serializer = serializer()

    return serializer


blank_serializer = create_serializer()
detail_serializer = create_serializer({"detail": serializers.CharField()})
