from categories.models import Store
from django.conf import settings
from django.contrib import admin


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
