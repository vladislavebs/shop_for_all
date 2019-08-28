from common.serializers import UserBasicSerializer
from shops.serializers import StoreBasicSerializer


class UserSerializer(UserBasicSerializer):
    store = StoreBasicSerializer(read_only=True)


class UserDetailSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        exclude = ("password", "groups", "user_permissions")
