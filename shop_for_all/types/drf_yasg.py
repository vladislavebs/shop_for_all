from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class SchemaViewType(APIView):
    # venv/lib/python3.7/site-packages/drf_yasg/views.py
    _ignore_model_permissions: bool
    schema: None
    public: bool
    generator_class: str
    authentication_classes: tuple
    permission_classes: tuple
    renderer_classes: tuple

    # noinspection PyShadowingBuiltins
    def get(self, request: Request, version: str = "", format: None = None) -> Response:
        pass

    @classmethod
    def apply_cache(
        cls, view: APIView, cache_timeout: int, cache_kwargs: dict
    ) -> APIView:
        pass

    @classmethod
    def as_cached_view(
        cls, cache_timeout: int = 0, cache_kwargs: dict or None = None, **initkwargs
    ) -> APIView:
        pass

    @classmethod
    def without_ui(
        cls, cache_timeout: int = 0, cache_kwargs: dict or None = None
    ) -> APIView:
        pass

    @classmethod
    def with_ui(
        cls,
        renderer: str = "swagger",
        cache_timeout: int = 0,
        cache_kwargs: dict or None = None,
    ) -> APIView:
        pass
