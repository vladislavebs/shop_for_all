from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from rest_framework.fields import JSONField

from shop_for_all.constants.models import MAX_LENGTH
from shop_for_all.helpers import models as models_helpers
from shop_for_all.helpers.django import USER_MODEL


#########
# Price #
#########


class PriceStatuses:
    ACTIVE = "active"

    STATUSES = ((ACTIVE, ACTIVE),)


class Price(models_helpers.BasicModel, models_helpers.GenericModel):
    price = models.FloatField()
    status = models.CharField(
        max_length=32, choices=PriceStatuses.STATUSES, default=PriceStatuses.ACTIVE
    )
    start_date = models.DateTimeField(blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    generic_related_name = "price"
    generic_on_delete = models.CASCADE
    limit_models = (
        ("products", "product"),
        ("shops", "storecategory"),
        ("shops", "storeproduct"),
    )

    class Meta:
        verbose_name = "price"
        verbose_name_plural = "prices"


class PriceLog(models.Model):
    status = models.CharField(
        max_length=32, choices=PriceStatuses.STATUSES, default=PriceStatuses.ACTIVE
    )
    new_data = JSONField()
    old_data = JSONField(allow_null=True)
    price = models.ForeignKey(
        to=Price, related_name="logs", on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = "price log"
        verbose_name_plural = "prices logs"


############
# WishList #
############


class WishList(models_helpers.BasicModel):
    name = models.CharField(max_length=MAX_LENGTH)
    codename = models.SlugField(max_length=MAX_LENGTH, blank=True, unique=True)
    user = models.ForeignKey(
        to=USER_MODEL, related_name="wishlists", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "wishlist"
        verbose_name_plural = "wishlists"


class ContentWishList(models_helpers.GenericModel):
    wishlist = models.ForeignKey(
        to=WishList, related_name="content", on_delete=models.CASCADE
    )

    generic_on_delete = models.CASCADE
    limit_models = (("products", "product"),)

    class Meta:
        verbose_name = "content wishlist"
        verbose_name_plural = "contents wishlists"


#############
# Relations #
#############

PRICES_RELATION = GenericRelation(to=Price)
