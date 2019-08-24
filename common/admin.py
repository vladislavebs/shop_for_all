from django.contrib import admin

from common import models

admin.site.register(models.PriceLog)


@admin.register(models.Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("get_content_object", "status", "price", "start_date", "end_date")

    @staticmethod
    def get_content_object(price: models.Price):
        return price.content_object.name

    get_content_object.short_description = "Name"
    get_content_object.admin_order_field = "content_object__name"


class WishlistContent(admin.TabularInline):
    model = models.ContentWishList


@admin.register(models.WishList)
class WishlistAdmin(admin.ModelAdmin):
    inlines = (WishlistContent,)
