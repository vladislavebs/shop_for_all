from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from rest_framework.fields import JSONField

from shop_for_all.constants.models import MAX_LENGTH
from shop_for_all.helpers.django import format_foreign_key_limit, USER_MODEL
from shop_for_all.helpers.models import BasicModel

PRICE_MODELS = format_foreign_key_limit(("products", "product"))
WISHLIST_MODELS = format_foreign_key_limit(("products", "product"))


class PriceStatuses:
    ACTIVE = "active"

    STATUSES = ((ACTIVE, ACTIVE),)


class Price(BasicModel, models.Model):
    price = models.FloatField()
    status = models.CharField(
        max_length=32, choices=PriceStatuses.STATUSES, default=PriceStatuses.ACTIVE
    )
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    content_type = models.ForeignKey(
        to=ContentType, on_delete=models.CASCADE, limit_choices_to=PRICE_MODELS
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        print(self.content_object.name)
        print(self.content_type)
        return ""


class PriceLog(models.Model):
    status = models.CharField(
        max_length=32, choices=PriceStatuses.STATUSES, default=PriceStatuses.ACTIVE
    )
    new_data = JSONField()
    old_data = JSONField(allow_null=True)
    price = models.ForeignKey(
        to=Price, related_name="logs", on_delete=models.DO_NOTHING
    )


class WishList(BasicModel, models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    codename = models.SlugField(max_length=MAX_LENGTH, blank=True, unique=True)
    user = models.ForeignKey(
        to=USER_MODEL, related_name="wishlists", on_delete=models.CASCADE
    )


class ContentWishList(models.Model):
    wishlist = models.ForeignKey(
        to=WishList, related_name="content", on_delete=models.CASCADE
    )

    content_type = models.ForeignKey(
        to=ContentType, on_delete=models.CASCADE, limit_choices_to=WISHLIST_MODELS
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
