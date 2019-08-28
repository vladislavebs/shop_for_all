from rest_framework import serializers

from common import models
from shop_for_all.helpers.django import USER_MODEL


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        exclude = (
            "last_login",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "groups",
            "user_permissions",
        )


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Price
        exclude = ("object_id", "content_type")
        extra_kwargs = {"status": {"read_only": True}}
