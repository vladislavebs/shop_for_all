from rest_framework import serializers

from shops import models
from users import serializers as users_serializers


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

    class Meta:
        model = models.Store
        exclude = ("categories", "products")
