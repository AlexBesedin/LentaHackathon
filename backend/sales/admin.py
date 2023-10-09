from django.contrib import admin

from .models import Sales, SalesRecord


@admin.register(SalesRecord)
class SalesRecordAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'sales_type',
        'sales_units',
        'sales_units_promo',
        'sales_rub',
        'sales_rub_promo',
    )
    search_fields = ['date']


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        'store',
        'sku',
    )
    search_fields = ['store__store__title', 'sku__sku']
