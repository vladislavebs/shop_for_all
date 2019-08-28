from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_extensions import mixins as extensions_mixins

from shop_for_all.helpers import filters_backends
from shop_for_all.helpers.django import USER_MODEL
from shop_for_all.helpers.rest import action
from shops.serializers import StoreSerializer
from users import serializers


class UsersView(extensions_mixins.NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = USER_MODEL.objects.all()
    serializer_class = serializers.UserSerializer

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


class UserView(viewsets.GenericViewSet):
    serializer_class = serializers.UserDetailSerializer
    pagination_class = None

    @action(methods=["GET"], detail=False)
    @swagger_auto_schema(responses={200: serializers.UserDetailSerializer(many=False)})
    def details(self, request: Request):
        user = request.user
        serializer = self.get_serializer(user)

        return Response(serializer.data)
