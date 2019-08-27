from rest_framework import viewsets
from rest_framework_extensions import mixins as extensions_mixins

from products import models, serializers
from shop_for_all.helpers import filters_backends


class CategoriesView(
    extensions_mixins.NestedViewSetMixin, viewsets.ReadOnlyModelViewSet
):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    filter_backends = (
        # filters_backends.ModelFieldsFilterBackend,
        filters_backends.OrderingFilter,
    )

    fields = ()

    ordering_fields = ("id", "name", "date_created")
    ordering = "id"


class ProductsView(extensions_mixins.NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    filter_backends = (
        # filters_backends.ModelFieldsFilterBackend,
        filters_backends.OrderingFilter,
    )

    fields = ()

    ordering_fields = ("id", "name", "price", "date_created")
    ordering = "id"
