from django.conf import settings
from django.contrib import admin
from stores.models import (City, Division, Location, Size, Store, Stores,
                           Type_format)


class StoresAdmin(admin.ModelAdmin):
    list_display = (
        'store',
    )
    search_fields = (
        'store',
    )
    list_filter = (
        'store',
    )
    ordering = ('store',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class CityAdmin(admin.ModelAdmin):
    list_display = (
        'city',
    )
    search_fields = (
        'city',
    )
    list_filter = (
        'city',
    )
    ordering = ('city',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class DivisionAdmin(admin.ModelAdmin):
    list_display = (
        'division',
    )
    search_fields = (
        'division',
    )
    list_filter = (
        'division',
    )
    ordering = ('division',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'loc',
    )
    search_fields = (
        'loc',
    )
    list_filter = (
        'loc',
    )
    ordering = ('loc',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class SizeAdmin(admin.ModelAdmin):
    list_display = (
        'size',
    )
    search_fields = (
        'size',
    )
    list_filter = (
        'size',
    )
    ordering = ('size',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class Type_formatAdmin(admin.ModelAdmin):
    list_display = (
        'type_format',
    )
    search_fields = (
        'type_format',
    )
    list_filter = (
        'type_format',
    )
    ordering = ('type_format',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'store',
        'city',
        'division',
        'type_format',
        'loc',
        'size',
        'is_active',
    )
    search_fields = (
        'store',
        'city',
        'division',
        'type_format',
        'loc',
        'size',
        'is_active',
    )
    list_filter = (
        'store',
        'city',
        'division',
        'type_format',
        'loc',
        'size',
        'is_active',
    )
    ordering = ('store',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


admin.site.register(Store, StoreAdmin)
admin.site.register(Stores, StoresAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Type_format, Type_formatAdmin)
