from django.contrib import admin

from .models import Store, StoreID


@admin.register(StoreID)
class StoreIDAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = [
        'store',
        'city',
        'division',
        'type_format',
        'loc',
        'size',
        'is_active',
    ]
    search_fields = [
        'store__store',
        'city',
        'division',
    ]
    list_filter = [
        'is_active',
        'city',
        'division',
        'type_format',
        'loc',
        'size',
    ]
    ordering = ['store']
