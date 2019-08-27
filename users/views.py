from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions import mixins as extensions_mixins

from shop_for_all.helpers import filters_backends
from shop_for_all.helpers.django import USER_MODEL
from shops.serializers import StoreSerializer
from users import serializers


class UserView(extensions_mixins.NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = USER_MODEL.objects.all()
    serializer_class = serializers.UserDetailSerializer

    filter_backends = (
        # filters_backends.ModelFieldsFilterBackend,
        filters_backends.OrderingFilter,
    )

    fields = ()

    ordering_fields = ("id", "username", "date_joined")
    ordering = "id"

    @action(methods=["GET"], detail=True)
    def store(self, *_, **__):
        store = self.get_object().store
        serializer = StoreSerializer(store)

        return Response(serializer.data)
