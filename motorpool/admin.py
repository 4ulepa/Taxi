from django.contrib import admin

from .models import Brand, Auto


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    pass
