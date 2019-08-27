from rest_framework import viewsets, mixins
from rest_framework.response import Response

from shop_for_all.helpers import filters_backends
from shop_for_all.helpers.rest import action
from shops import models, serializers


class StoresView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer

    filter_backends = (
        # filters_backends.ModelFieldsFilterBackend,
        filters_backends.OrderingFilter,
    )

    fields = ()

    ordering_fields = ("id", "name", "date_created")
    ordering = "id"


class UserStoreView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    pagination_class = None
    serializer_class = serializers.StoreSerializer

    @action(methods=["GET"], detail=False)
    def details(self, request):
        store = models.Store.objects.get(user=request.user)
        serializer = serializers.StoreSerializer(store)

        return Response(serializer.data)

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=serializers.StoreProductsSerializer,
    )
    def product(self, request):
        store = models.Store.objects.get(user=request.user)
        serializer = serializers.StoreProductsSerializer(
            instance=store, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response()
