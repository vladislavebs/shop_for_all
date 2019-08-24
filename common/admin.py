from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from common import models


@admin.register(models.PriceLog)
class PriceLogAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("get_content_object", "status", "price", "start_date", "end_date")

    @staticmethod
    def get_content_object(price: models.Price):
        return price.content_object.name

    get_content_object.short_description = "Name"
    get_content_object.admin_order_field = "content_object__name"


class WishListContent(GenericTabularInline):
    model = models.ContentWishList


@admin.register(models.WishList)
class WishlistAdmin(admin.ModelAdmin):
    inlines = (WishListContent,)
