from rest_framework import serializers

from shops import models
from products import models as products_models
from users import serializers as users_serializers
from common import serializers as common_serializers


class StoreProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreProduct
        fields = "__all__"


class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreCategory
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    user = users_serializers.UserSerializer(read_only=True)

    def create(self, validated_data):
        store, created = models.Store.objects.update_or_create(
            user=self.context["request"].user, defaults=validated_data
        )

        return store

    class Meta:
        model = models.Store
        exclude = ("categories", "products", "codename")
        extra_kwargs = {
            "date_created": {"read_only": True},
            "user": {"read_only": True},
        }


# noinspection PyAbstractClass
class StoreProductsSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=products_models.Product.objects.all()
    )
    price = serializers.FloatField()
    prices = common_serializers.PriceSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        pass
