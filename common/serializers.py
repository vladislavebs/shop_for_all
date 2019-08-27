from rest_framework import serializers

from common import models


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Price
        exclude = ("object_id", "content_type")
        extra_kwargs = {"status": {"read_only": True}}
