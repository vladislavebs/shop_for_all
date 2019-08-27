from rest_framework import serializers

from shop_for_all.helpers.django import USER_MODEL


class UserSerializer(serializers.ModelSerializer):
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


class UserDetailSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        exclude = ("password", "groups", "user_permissions")
