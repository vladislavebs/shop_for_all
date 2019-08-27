from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from common import models
from shop_for_all.helpers.admin import GenericModelAdmin


@admin.register(models.PriceLog)
class PriceLogAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Price)
class PriceAdmin(GenericModelAdmin):
    list_display = (
        "content_object",
        "show_content_type",
        "status",
        "price",
        "start_date",
        "end_date",
    )


class WishListContent(GenericTabularInline):
    model = models.ContentWishList


@admin.register(models.WishList)
class WishlistAdmin(admin.ModelAdmin):
    inlines = (WishListContent,)
