import typing

from drf_yasg import openapi, renderers
from drf_yasg.views import get_schema_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from shop_for_all import settings
from shop_for_all.env import DEBUG
from shop_for_all.types.drf_yasg import SchemaViewType

AUTO_SCHEMA_KEY = "_swagger_auto_schema"


def update_auto_schema(view, data):
    auto_schema = getattr(view, AUTO_SCHEMA_KEY, {})

    new_schema = {**auto_schema, **data}
    setattr(view, AUTO_SCHEMA_KEY, new_schema)

    return new_schema


def available_filter_values(values: typing.Iterable[str]):
    return f"<i>Available values</i> : {', '.join(values)}."


def basic_action(method=None, detail=False, filter_backends=None):
    return {
        "detail": detail,
        "methods": [method] if method else None,
        "pagination_class": None,
        "filter_backends": filter_backends,
        "serializer_class": None,
    }


# noinspection PyTypeChecker
_SchemaView: SchemaViewType = get_schema_view(
    public=True,
    authentication_classes=(TokenAuthentication,),
    permission_classes=(AllowAny,),
    info=openapi.Info(
        title=settings.API_NAME,
        default_version=settings.API_VERSION,
        description=settings.API_DESCRIPTION,
    ),
)


class SchemaView(_SchemaView):
    renderer_classes = (
        renderers.SwaggerYAMLRenderer,
        renderers.OpenAPIRenderer,
        renderers.ReDocRenderer,
        renderers.SwaggerJSONRenderer,
    )

    @classmethod
    def without_ui(cls, cache_timeout=0, cache_kwargs=None):
        return cls.as_cached_view(
            cache_timeout=cache_timeout,
            cache_kwargs=cache_kwargs,
            renderer_classes=cls.renderer_classes,
        )


timeout_cache = 0 if DEBUG else 3600
docs_with_ui = SchemaView.with_ui(cache_timeout=timeout_cache)
docs_without_ui = SchemaView.without_ui(cache_timeout=timeout_cache)
