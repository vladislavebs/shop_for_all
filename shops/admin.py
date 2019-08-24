from django.contrib import admin

from shops import models


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    pass
