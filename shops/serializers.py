from django.utils import timezone
from rest_framework import serializers

from common import serializers as common_serializers
from products import models as products_models
from products.serializers import ProductSerializer
from shop_for_all.helpers.methods import unpack
from shops import models


class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreCategory
        fields = "__all__"


class StoreBasicSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        store, created = models.Store.objects.update_or_create(
            user=self.context["request"].user, defaults=validated_data
        )

        return store

    class Meta:
        model = models.Store
        basic_exclude = ("categories", "products", "codename")
        exclude = (*basic_exclude, "user")
        extra_kwargs = {
            "date_created": {"read_only": True},
            "user": {"read_only": True},
        }


class StoreSerializer(StoreBasicSerializer):
    user = common_serializers.UserBasicSerializer(read_only=True)

    class Meta(StoreBasicSerializer.Meta):
        exclude = StoreBasicSerializer.Meta.basic_exclude


class StoreProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=products_models.Product.objects.all()
    )
    price = serializers.FloatField()
    product = ProductSerializer(read_only=True)
    store = StoreSerializer(read_only=True)

    class Meta:
        model = models.StoreProduct
        fields = "__all__"


# noinspection PyAbstractClass
class UserStoreProductSerializer(StoreProductSerializer):
    store = None
    prices = common_serializers.PriceSerializer(many=True, required=False)

    class Meta(StoreProductSerializer.Meta):
        fields = None
        exclude = ("store",)

    @staticmethod
    def validate_prices(prices):
        errors = {}

        for index, price in enumerate(prices):
            start_date, end_date = unpack(price, "start_date", "end_date")

            error = {}

            start_date < timezone.now() and error.update(
                {"start_date": ["Start date cannot be in past."]}
            )

            end_date < timezone.now() and error.update(
                {"end_date": ["End date cannot be in past."]}
            )

            start_date >= end_date and error.update(
                {"non_field_errors": ["End date must be greater that start date."]}
            )

            error and errors.update({index: error})

        if errors:
            raise serializers.ValidationError(errors)

        return prices

    def update(self, store: models.Store, validated_data: dict):
        product, price, prices = unpack(validated_data, "product_id", "price", "prices")
        return store.add_product(product=product, basic_price=price, prices=prices)
