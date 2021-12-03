from django.contrib import admin

from .models import Brand, Auto, Option


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    pass


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass
