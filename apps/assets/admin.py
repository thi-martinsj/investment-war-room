from django.contrib import admin

from .models import Assets, AssetsConfig, AssetsValues


class AssetsAdmin(admin.ModelAdmin):
    list_display = ("id", "ticker")
    list_display_links = ("id", "ticker")
    search_fields = ("ticker", "name")
    list_per_page = 20


class AssetsConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "asset_id", "user_id","min_value",
                    "max_value", "frequency", "is_active")
    list_display_links = ("id", "asset_id")
    search_fields = ("asset_id",)
    list_filter = ("is_active",)
    list_per_page = 20
    list_editable = ("is_active",)


class AssetsValuesAdmin(admin.ModelAdmin):
    list_display = ("id", "asset_id", "value")
    list_display_links = ("id", "asset_id")
    search_fields = ("asset_id",)
    list_per_page = 50


admin.site.register(Assets, AssetsAdmin)
admin.site.register(AssetsConfig, AssetsConfigAdmin)
admin.site.register(AssetsValues, AssetsValuesAdmin)
